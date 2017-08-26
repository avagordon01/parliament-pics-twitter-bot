import sys
import gi
gi.require_version('Gst', '1.0')
import gi.repository.Gst as gst
import streamlink
import time


import twitter
api = twitter.Api(
    consumer_key='LcYC92wtyaEUmAJrn9DGpiMv9',
    consumer_secret='kySXUeSJvcUuBWGibPItZL4GWwUypkfF4bm6fJ5w5u6o5C4UqU',
    access_token_key='888817867612971008-akD3ufr4QLhQCGUmpNv4qD3WdbGQcUZ',
    access_token_secret='EuiJrj9L3pcEBQ4DQKVk1xwtklkttlT9AavUgM1Lay9NO'
)
api.VerifyCredentials()
#api.PostMedia('status', 'filename.png')





gst.init(None)

url = 'http://bbc.co.uk/iplayer/live/bbcone'
quality = 'worst'

sl = streamlink.Streamlink()

try:
    streams = sl.streams(url)
except streamlink.NoPluginError:
    print("Streamlink is unable to handle the URL '{0}'".format(url))
    sys.exit()
except streamlink.PluginError as err:
    print("Plugin error: {0}".format(err))
    sys.exit()
if not streams:
    print("No streams found on URL '{0}'".format(url))
    sys.exit()
if quality not in streams:
    print("Unable to find '{0}' stream on URL '{1}'".format(quality, url))
    sys.exit()
stream = streams[quality]


def on_source_setup(element, source):
    # When this callback is called the appsrc expects
    # us to feed it more data
    source.connect("need-data", on_source_need_data)

def on_source_need_data(source, length):
    # Attempt to read data from the stream
    try:
        data = fd.read(length)
    except IOError as err:
        print("Failed to read data from stream: {0}".format(err))
        sys.exit()

    # If data is empty it's the end of stream
    if not data:
        source.emit("end-of-stream")
        return

    # Convert the Python bytes into a GStreamer Buffer
    # and then push it to the appsrc
    buf = gst.Buffer.new_wrapped(data)
    source.emit("push-buffer", buf)


# This creates a playbin pipeline and using the appsrc source
# we can feed it our stream data
pipeline = gst.ElementFactory.make("playbin", None)
pipeline.set_property("uri", "appsrc://")
# When the playbin creates the appsrc source it will call
# this callback and allow us to configure it
pipeline.connect("source-setup", on_source_setup)
freeze = gst.ElementFactory.make("imagefreeze", "freeze")
sink = gst.ElementFactory.make("ximagesink", "imagesink")
pipeline.add(freeze)
pipeline.add(sink)


# Attempt to open the stream
try:
    fd = stream.open()
except streamlink.StreamError as err:
    print("Failed to open stream: {0}".format(err))
    sys.exit()

# Start playback
pipeline.set_state(gst.State.PLAYING)


while True:
    print("test")
    pipeline.set_state(gst.State.READY)
    pipeline.set_state(gst.State.PLAYING)
    time.sleep(1)
