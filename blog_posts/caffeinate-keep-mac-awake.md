title: Keep Your Mac Awake with caffeinate
date: 2024-12-23
tags: mac, terminal, automation, tips
---

# Keep Your Mac Awake with caffeinate

I was running my [nuke-slack](https://github.com/sek3b/nuke-slack) script to clean up thousands of messages across multiple Slack workspaces. The script handles rate limiting automatically, which means it can take hours to complete.

The problem? My MacBook kept going to sleep.

Every time I walked away, the display would sleep, then the system would sleep, and my script would stall. I'd come back expecting progress and find it frozen mid-execution.

## The Solution: caffeinate

macOS has a built-in command called `caffeinate` that prevents your Mac from sleeping. No third-party apps needed.

```bash
caffeinate -d python3 ./nuke-slack.py
```

That's it. The `-d` flag prevents the display from sleeping, which also keeps the system awake.

## How It Works

`caffeinate` creates an assertion that tells macOS to stay awake. When your command finishes, the assertion is released and normal sleep behavior resumes.

The flags you'll actually use:

- `-d` - Prevent display sleep (what I use most)
- `-i` - Prevent idle sleep
- `-s` - Prevent system sleep (even on AC power)
- `-u` - Declare user activity (resets idle timer)

You can combine them:

```bash
caffeinate -di python3 ./long-running-script.py
```

## Other Use Cases

Any long-running task benefits from this:

```bash
# Large file downloads
caffeinate -d curl -O https://example.com/huge-file.zip

# Database migrations
caffeinate -d python3 manage.py migrate

# Video encoding
caffeinate -d ffmpeg -i input.mp4 -c:v libx264 output.mp4

# Backups
caffeinate -d rsync -av ~/Documents /Volumes/Backup/
```

## Time-Limited Caffeination

If you want to keep your Mac awake for a specific duration:

```bash
# Stay awake for 1 hour (3600 seconds)
caffeinate -d -t 3600
```

## Why Not Just Change Energy Settings?

You could go to System Settings and crank up the sleep timer, but:

1. You'll forget to change it back
2. It affects all usage, not just this one task
3. `caffeinate` is automatic - it ends when your command ends

## A Note on MDM-Managed Devices

If you're using a work laptop, your company's MDM (Mobile Device Management) may enforce sleep timers. These policies exist for good reason - an unlocked laptop at the office or coffee shop is a security risk.

But when you're at home with no one around, those security concerns don't apply. You want your device to stay running while you do other things around the house.

`caffeinate` lets you override the sleep behavior temporarily without fighting your IT department's policies. The script runs, the Mac stays awake, and when it's done everything goes back to normal. No policy violations, no permanently changed settings.

## The Takeaway

Next time you have a script that needs to run uninterrupted, prefix it with `caffeinate -d`. Your Mac stays awake exactly as long as needed, then goes back to normal.

Simple. Built-in. No apps required.
