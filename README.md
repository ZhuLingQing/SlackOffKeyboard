# SlackOffKeyboard
## Brief
Utilize RaspberryPi - Zero W USB-OTG to emulate a USB-HID keyboard.  
利用树莓派ZeroW 的USB-OTG功能，枚举成一个USB-HID键盘。然后模拟按键操作。  
参考：https://github.com/Sucareto/RPI_GPIO_HID_Keyboard

## How to use
`sudo bash Setup/USB_Setup.sh`  
会自动配置出一个HID-Keyboard设备。  
`python3 slack_off.py [text_file]`  
会自动讲整篇文本作为源用虚拟键盘进行输入。  

## TO DO
- 不同脚本类型的自动缩进调整  
- Automatic indent adjustment for different script types  
- 模拟人工输入的错误输入场景  
- Simulate the error input scenario of manual input  
- 更真实的输入频率调整
- More realistic input frequency adjustment