from getscreentag import get_result
from findbytags import get_gy_with_level

import time
last = None
while True:
    
    t =  get_result()
    if t and t != last:
        print('\033[7;35;46m ' + '检测到tag:' + ' '.join(t) + '\033[0m' )
        last = t
        gys = get_gy_with_level(t)
        for gy in gys:
            if gy[1] and gy[2] >= 4:
                print(gy[2],'\033[1;35;46m '+ ' '.join(gy[0]) +' \033[0m',gy[1])
            elif gy[1]:
                print(gy[2],gy[0],gy[1])
        print(' ')
        
    time.sleep(1)
