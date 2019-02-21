 
import func_img_process as f_ip

img_processor0 = f_ip.img_processor()
img_processor0.load_time_str()


for iteration in range(0,1000):
    img_processor0.find_next_idx()
    img_processor0.load_img()
    img_processor0.locate_ball(iteration)
    img_processor0.save_img()
    
     
    
    
    
    
    
     