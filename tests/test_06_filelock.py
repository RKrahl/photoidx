"""Concurrent access to the index file.

The Index class is supposed to protect the index file against
conflicts in concurrent file access using file system locking.
We will need multiple processes to test this.
"""

import filecmp
from multiprocessing import Process, Queue
import shutil
import pytest
import photoidx.index
import photoidx.idxfilter
from conftest import tmpdir, gettestdata

testimgs = [ 
    "dsc_4623.jpg", "dsc_4664.jpg", "dsc_4831.jpg", 
    "dsc_5126.jpg", "dsc_5167.jpg" 
]
testimgfiles = [ gettestdata(i) for i in testimgs ]
refindex = gettestdata("index-tagged.yaml")

# tags to test and expected results.
tags = {
    "Shinto_shrine": ["dsc_4664.jpg", "dsc_4831.jpg"],
    "Tokyo": ["dsc_4623.jpg", "dsc_4664.jpg"],
}

@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, str(tmpdir))
    shutil.copy(refindex, str(tmpdir / ".index.yaml"))
    return tmpdir

# --------------------------------------------------------------------
# Worker functions to be run in the subprocesses.  It does not really
# matter what we do here.  We just want two examples doing some
# readonly and some write access to the index file respectively.
#
# We use queues to synchronize in order to make sure the concurrent
# invocations access the index really at the same moment.

def ls_bytag(imgdir, tag, qres, qwait):
    """List files by tag.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter(tags=tag)
        qres.put((tag, [ str(i.filename) for i in idxfilter.filter(idx) ]))
        qwait.get()

def add_tag(imgdir, tag, qres):
    """Add a tag to all items.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        for i in idx:
            i.tags.add(tag)
        try:
            idx.write()
        except Exception as e:
            qres.put(e)
        else:
            qres.put("Done")

# --------------------------------------------------------------------

def test_concurrent_read(imgdir):
    """Test concurrent read access.
    Should work without problem.
    """
    qres = Queue()
    qwait = Queue()
    procs = []
    for t in tags.keys():
        p = Process(target=ls_bytag, args=(imgdir, t, qres, qwait))
        p.start()
        procs.append(p)
    print("Reading processes started.")
    for i in range(len(procs)):
        (t, files) = qres.get()
        assert files == tags[t]
    print("Replys from reading processes received.")
    # At this point, all subprocesses have the index file open for
    # reading: they sent a reply, so they have opened it, but they
    # still wait for the message on qwait, so they have not yet closed
    # it.
    for i in range(len(procs)):
        qwait.put("done")
    print("Joining processes.")
    for p in procs:
        p.join()

def test_concurrent_read_write(imgdir):
    """Test writing the index while another process is reading it.
    This should fail.
    """
    qresr = Queue()
    qresw = Queue()
    qwait = Queue()
    procs = []
    p = Process(target=ls_bytag, args=(imgdir, "Tokyo", qresr, qwait))
    p.start()
    procs.append(p)
    print("Reading process started.")
    (t, files) = qresr.get()
    assert files == tags[t]
    print("Reply from reading process received.")
    # At this point, the first subprocesse has the index file open for
    # reading and waits for the message on qwait.  Start the second
    # one that tries to write it.
    p = Process(target=add_tag, args=(imgdir, "all", qresw))
    p.start()
    procs.append(p)
    print("Writing process started.")
    # Verify that the writing process caught an AlreadyLockedError.
    r = qresw.get()
    assert isinstance(r, photoidx.index.AlreadyLockedError)
    print("Reply from writing process received.")
    # Now, allow the reading process to close the index file.
    qwait.put("done")
    print("Joining processes.")
    for p in procs:
        p.join()
    # Finally, verify that the index is still unchanged, so the
    # writing did not succeed.
    idxfile = str(imgdir / ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"
