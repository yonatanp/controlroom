#!/home/hd26/seftembr/.virtualenvs/potions/bin/python
import os
import sys
import subprocess
import math
import datetime
from potion import potion
from potion import TextArgument, MultilineArgument, ChoiceArgument, BooleanArgument
from potion import ScriptBlueprint, ScriptMetadata

# ~~~ get subtitles

def title(accept_nonstrict_match=False):
    script = "title" if not accept_nonstrict_match else "titleeeee"
    command_line = os.path.join(os.environ["HOME"], script)
    sp = subprocess.Popen(command_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = sp.communicate()
    sys.stdout.write(out); sys.stdout.flush()
    sys.stderr.write(err); sys.stderr.flush()

title = ScriptBlueprint(
    "title",
    __name__,
    metadata=ScriptMetadata("title"),
    arguments=[
        BooleanArgument("accept_nonstrict_match"),
    ],
    main=title
)

potion.registerScript(title, '/title')

# ~~~ download torrents

def add_torrent(magnet_url):
    from deluge_client import DelugeRPCClient
    client = DelugeRPCClient('127.0.0.1', 2196, "seftembr", "TuGsFYqlNP")
    client.connect()
    result = client.call('core.add_torrent_magnet', magnet_url, {})
    print "Returned hash:", result

potion.registerScript(ScriptBlueprint('torrent_add', 'torrent_add', metadata=ScriptMetadata("Add Torrent"), arguments=[TextArgument("magnet_url", required=True)], main=add_torrent), '/torrent_add')

def torrents_status():
    STATUS_KEYS = [
    "state",
    "download_location",
    "tracker_host",
    "tracker_status",
    "next_announce",
    "name",
    "total_size",
    "progress",
    "num_seeds",
    "total_seeds",
    "num_peers",
    "total_peers",
    "eta",
    "download_payload_rate",
    "upload_payload_rate",
    "ratio",
    "distributed_copies",
    "num_pieces",
    "piece_length",
    "total_done",
    "files",
    "file_priorities",
    "file_progress",
    "peers",
    "is_seed",
    "is_finished",
    "active_time",
    "seeding_time"
    ]
    from deluge_client import DelugeRPCClient
    client = DelugeRPCClient('127.0.0.1', 2196, "seftembr", "TuGsFYqlNP")
    client.connect()
    print "--- ACTIVE ---"
    for (hashid, fields) in client.call('core.get_torrents_status', {"state":"Active"}, STATUS_KEYS).iteritems():
        print "%s: %s (%.2f out of %s - active for %s so far)" % (hashid, fields['name'], fields['progress'], sizeof_fmt(fields['total_size']), human_time(seconds=fields['active_time']))
    print "--- PAUSED ---"
    for (hashid, fields) in client.call('core.get_torrents_status', {"state":"Paused"}, STATUS_KEYS).iteritems():
        if fields['progress'] == 100:
            print "%s: %s (%s downloaded in %s)" % (hashid, fields['name'], sizeof_fmt(fields['total_size']), human_time(seconds=fields['active_time']))
        else:
            print "%s: %s (%.2f out of %s - was active for %s - and paused)" % (hashid, fields['name'], fields['progress'], sizeof_fmt(fields['total_size']), human_time(seconds=fields['active_time']))

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def human_time(*args, **kwargs):
    secs  = float(datetime.timedelta(*args, **kwargs).total_seconds())
    units = [("day", 86400), ("hour", 3600), ("minute", 60), ("second", 1)]
    parts = []
    for unit, mul in units:
        if secs / mul >= 1 or mul == 1:
            if mul > 1:
                n = int(math.floor(secs / mul))
                secs -= n * mul
            else:
                n = secs if secs != int(secs) else int(secs)
            parts.append("%s %s%s" % (n, unit, "" if n == 1 else "s"))
    return ", ".join(parts)

potion.registerScript(ScriptBlueprint('torrents_status', 'torrents_status', metadata=ScriptMetadata("Torrents Status"), arguments=[], main=torrents_status), '/torrents_status')

potion.run(port=7666)

