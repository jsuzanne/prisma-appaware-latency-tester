# Configuration Guide

## Server Configuration

### Location
/etc/systemd/system/tcp-server.service

text

### Parameters

ExecStart=/usr/bin/python3 /opt/tcp-server/server.py
--host 0.0.0.0
--port 18890
--delay-min 5
--delay-max 10
--data-size 104857600

text

### Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--host` | 0.0.0.0 | IP to bind (0.0.0.0 = all interfaces) |
| `--port` | 8888 | Listening port |
| `--delay-min` | 5 | Minimum processing delay (seconds) |
| `--delay-max` | 10 | Maximum processing delay (seconds) |
| `--data-size` | 1048576 | Payload size in bytes |

### Common Scenarios

#### Fast Application (< 1 second)
--delay-min 0.5
--delay-max 1
--data-size 1048576

text

#### Slow Application (Current)
--delay-min 5
--delay-max 10
--data-size 104857600

text

#### Very Slow Application
--delay-min 15
--delay-max 30
--data-size 1048576000

text

### Apply Changes

sudo systemctl daemon-reload
sudo systemctl restart tcp-server
sudo journalctl -u tcp-server -f

text

---

## Client Configuration

### Location
/opt/tcp-client/serverXX.env

text

### Format

HOST=192.168.1.201
PORT=18890

text

### Multiple Servers

Server 1
sudo nano /opt/tcp-client/server01.env
HOST=192.168.1.201
PORT=18890

Server 2
sudo nano /opt/tcp-client/server02.env
HOST=192.168.1.202
PORT=18890

Server 3
sudo nano /opt/tcp-client/server03.env
HOST=192.168.1.203
PORT=18890

text

### Start Multiple Clients

sudo systemctl start tcp-client@server01
sudo systemctl start tcp-client@server02
sudo systemctl start tcp-client@server03

sudo systemctl enable tcp-client@server01
sudo systemctl enable tcp-client@server02
sudo systemctl enable tcp-client@server03

text

### View Logs for Each

Server 1
sudo journalctl -u tcp-client@server01 -f

Server 2
sudo journalctl -u tcp-client@server02 -f

All at once
sudo journalctl -u tcp-client@* -f

text

---

## Business Hours Configuration

### Current Behavior

The client automatically adjusts activity based on time:

| Time | Day | Interval | Behavior |
|------|-----|----------|----------|
| 8h-18h | Mon-Fri | 2-3 min | Active users |
| 10h, 14h, 16h | Mon-Fri | 1.5-2 min | Peak hours |
| 12h, 17h | Mon-Fri | 4-7 min | Lunch/end of day |
| 18h-8h | Mon-Fri | 10-30 min | Night batch jobs |
| All day | Sat-Sun | 30-60 min | Weekend minimal |

### Modify Base Interval

Edit `/opt/tcp-client/client.py`:

parser.add_argument('--interval', type=float, default=180.0)

text

Change `180.0` to:
- `60.0` = More frequent (1 min base)
- `300.0` = Less frequent (5 min base)

Then restart:
sudo systemctl restart tcp-client@server01

text

---

## Firewall Configuration

### Server Side (Ubuntu201)

Allow incoming on port 18890
sudo ufw allow 18890/tcp

Verify
sudo ufw status

text

### Client Side (Ubuntu207)

No firewall changes needed (outbound connections only).

---

## Monitoring

### Check Service Status

Server
sudo systemctl status tcp-server

Client
sudo systemctl status tcp-client@server01

text

### View Live Logs

Server
sudo journalctl -u tcp-server -f

Client
sudo journalctl -u tcp-client@server01 -f

text

### Count Transactions

Total transactions today
sudo journalctl -u tcp-client@server01 --since today | grep "Transaction #" | wc -l

Average transaction time
sudo journalctl -u tcp-client@server01 --since today |
grep "Temps de transaction" |
awk '{print $9}' |
awk '{sum+=$1; n++} END {print "Average:", sum/n, "seconds"}'

text

---

## Troubleshooting

### Server won't start

Check errors
sudo journalctl -u tcp-server -n 50

Check if port is already used
sudo netstat -tlnp | grep 18890

Test manually
sudo /opt/tcp-server/server.py --port 18890

text

### Client can't connect

Test network
ping <server-ip>

Test port
nc -zv <server-ip> 18890
telnet <server-ip> 18890

Check firewall
sudo ufw status

text

### High CPU usage

Check process
top -p $(pgrep -f tcp-server)

Reduce data size in server config
sudo nano /etc/systemd/system/tcp-server.service

Change: --data-size 10485760 (10 MB instead of 100 MB)
text

---

## Advanced Configuration

### Change Client User-Agent

Edit `/opt/tcp-client/client.py`:

message = f"Request #{iteration} - {now.strftime('%Y-%m-%d %H:%M:%S')}"

text

Add custom identifier for tracking.

### Disable Business Hours Logic

Edit `/opt/tcp-client/client.py`, find:

dynamic_interval = get_dynamic_interval(interval)

text

Replace with:

dynamic_interval = interval # Fixed interval

text

---

## Best Practices

1. **Start with default settings** for initial demos
2. **Adjust delay** to match customer's slow applications
3. **Use multiple clients** to show concurrent users
4. **Monitor Prisma dashboard** during traffic generation
5. **Document changes** for reproducibility

---

**Need Help?**

Open an issue: https://github.com/jsuzanne/prisma-appaware-latency-tester/issues
