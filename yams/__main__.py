import sys
import argparse
import rxv
import alexandra

app = alexandra.Application()


def get_receiver():
    try:
        return rxv.find()[0]
    except:
        print("No receiver found!")
        sys.exit(1)

receiver = get_receiver()


def server(port, debug):
    if debug:
        app.run_debug('0.0.0.0', port)
    else:
        app.run('0.0.0.0', port, debug=False)


@app.intent('SetVolume')
def set_volume(slots, session):
    direction = slots['Direction']
    valid_tweaks = ['a lot', 'a bunch', 'a little', 'a bit', 'a tad']
    tweak = slots.get('VolumeTweak', "")
    if tweak not in valid_tweaks:
        tweak = ''
    current_volume = receiver.volume
    if tweak == "a lot" or tweak == "a bunch":
        vol = 10.0
    elif tweak == "a little" or tweak == "a bit" or tweak == "a tad":
        vol = 2.0
    else:
        vol = 5.0

    if direction == 'up':
        new_volume = current_volume + vol
        if new_volume >= -100:
            receiver.volume = new_volume
            return alexandra.respond("Turning it up {}".format(tweak))
        else:
            return alexandra.respond("Can't turn it up this high")
    else:
        new_volume = current_volume - vol
        if new_volume <= -1:
            receiver.volume = new_volume
            return alexandra.respond("Turning it down {}".format(tweak))
        else:
            return alexandra.respond("Can't turn it down this low")


@app.intent("SetPowerState")
def set_state(slots, session):
    state = slots['State']
    if state in ['on', 'off']:
        receiver.on = state == "on"
        return alexandra.respond("Powering {}".format(state))
    else:
        return alexandra.respond("You need to tell me to power on or off")


def set_input(req):
    pass


if __name__ == '__main__':
    description = "Yamaha receiver controller for Amazon Echo devices"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-p', '--port',
                        type=int,
                        default=8185,
                        help="Port to run the server on.")
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    server(args.port, args.debug)
