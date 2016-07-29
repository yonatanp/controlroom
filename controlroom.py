#!/home/hd26/seftembr/.virtualenvs/potions/bin/python
import os
import sys
import subprocess
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
    client = DelugeRPCClient('127.0.0.1', 2196, u, "TuGsFYqlNP")
    client.connect()
    result = client.call('core.add_torrent_magnet', magnet_url, {})
    print "Returned hash:", result

potion.registerScript(ScriptBlueprint('torrent_add', 'torrent_add', metadata=ScriptMetadata("Add Torrent"), arguments=[TextArgument("magnet_url", required=True)], main=add_torrent), '/torrent_add')


potion.run(port=7666)

