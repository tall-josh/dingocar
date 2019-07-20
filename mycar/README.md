# How to Train Responsibly

These are the steps to follow from gather data (manually drive) to training to driving with an Neural Network.

## On your local machine

### Onetime setup

1. Make sure your running an ssh server on your local machine. If not intall it.

```
sudo apt-get update
sudo apt-get install openssh-server
```

2. Add your own public key to authorized keys

```
cat ~/.ssh/id_rsa.pub >> authorized_keys
```

### Shh to pi, with the right args.

1. ssh to the pi with `-AR`. `A` will forward with you're local credentials. The
`R 2050` will forward a port from the Pi back to your local machine. This will allow
our scrips on the Pi `scp` (secure copy) files back to your loacl machine once you
are done driving.

```
ssh -AR 2050:localhost:22 pi@roba1.local

# Now you're on the Pi
```

### Gather driving data

**On the Pi**

0. `cd play/roba1/mycar`

1. Fill in the `info.json`: The `info.json` is used to help keep track of when a dataset was gathers and what type of data is in the tub that is gathered. I recomend you fill this is at the start of a labelling session (or whenever your track or track  environment changes). A sample `info.json` is below:

```
{
  "count"       : SET AUTOMATICALLY,
  "date"        : SET AUTOMATICALLY,
  "tape"        : "thick yellow",
  "floor"       : "timber",
  "location"    : "bill gates' house",
  "centre line" : true,
  "lane width"  : "40cm"
}
```

2. Edit some variables in `save_tub.sh`. See the comments for more info.

3. Drive the car manually to gather data. Ideally for 8-10 laps in each
   direction. Run `python manage.py drive`. The frames and control data
   will be stored in `tub`.

4. Use the `save_tub.sh` scrip, pass a message in "doube quotes"
```
./save_tub.sh "This is a sample message"
```
