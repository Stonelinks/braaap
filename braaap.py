#~ braaap.py
#~ an irritating system activity monitor
#~ plays audio that sounds like a crappy 8-bit car engine
#~ the higher the engine revs, the harder your CPU is working

import sys
import random
import subprocess
import psutil

def run_bash(cmd):
  """
  Run a bash command and return the result.
  """
  p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=sys.stderr)
  p.wait()
  return p.communicate()[0].strip()

def scale(val, src, dst):
  """
  Scale the given value from the scale of src to the scale of dst.
  """
  return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

if __name__ == "__main__":
  if 'run' in sys.argv:
  
    fast = 4.0
    slow = 162.0

    #~ current_speed = int((fast + slow) / 2)
    current_speed = slow
    time = 1

    cpu = psutil.cpu_percent(None)
    terminal_width = int(run_bash('stty size').split()[1])

    while True:
      
      #~ this produces a crappy engine noise depending on speed
      if time % int(current_speed) == 0:
        sound = unicode(0x00)
      elif time % int(current_speed) == 3:
        sound = unicode(int(random.uniform(0x00, 0xff)))
      else:
        sound = unicode(0x09)

      #~ update speed based on CPU usage
      if time % 5000 * current_speed == 0:
        cpu = psutil.cpu_percent(None)
        current_speed = scale(cpu, (0.0, 100.0), (slow, fast))
        
        #~ make sure we stay in the speed limits!
        current_speed = max(min(current_speed, slow), fast)

      if time % 1000 == 0 and time > 100000:
        
        #~ print a load bar in the terminal
        chars = int(scale(cpu, (0.0, 100.0), (0.0, float(terminal_width))))
        sys.stderr.write((chars * '*') + '\n')
        #~ sys.stderr.write(unicode(current_speed) + '\n')
        
      sys.stdout.write(sound)
      time += 1
  else:
    def test_play_method(method):
      return len(run_bash('which ' + method)) > 0
    
    def play(cmd):
      play_cmd = 'python ' + __file__ + ' run | ' + cmd
      print play_cmd
      subprocess.call(play_cmd, shell=True)
    
    if test_play_method('mplayer'):
      play('mplayer -quiet -rawaudio samplesize=1:channels=1:rate=8000:bitrate=64000 -demuxer rawaudio -')
    elif test_play_method('aplay'):
      play('aplay')
    elif test_play_method('pacat'):
      play('pacat --format u8 --rate 8000')
