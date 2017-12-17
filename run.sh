trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

streamlink https://www.twitch.tv/faceit_tv2 best -p 'mpv --no-audio --vo=image --vf=lavfi=[fps=1/5] --vo-image-outdir=out' &

python3 -B bot.py &

wait -n
kill $(jobs -p) || true
