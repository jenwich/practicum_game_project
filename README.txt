ชื่อโครงงาน: Let's hunt the little bears!

ชื่อทีม: สามเกลอเจอหมี
สมาชิก:
	1. 5710500178 นายเจนวิชญ์ รัตนเย็นใจ
	2. 5710503444 นายปูรณสิทธิ์ ปิยวัชรวิจิตร
	3. 5710503487 นายภาณุพงศ์ มณีรัตน์
วิชาการปฏิบัติการทางวิศวกรรมคอมพิวเตอร์ ภาควิชาวิศวกรรมคอมพิวเตอร์ คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์

รายละเอียดโครงงาน:
เกมยิงธนูล่าหมี สามารถบังคับตัวละครให้เคลื่อนที่ซ้ายขวาได้ สามารถปรับความแรงและองศาของการยิง และเป่าที่เซนเซอร์รับเสียงเพื่อกำจัดหมีทั้งหมดออกไป

ภาษาที่ใช้ในการพัฒนา
	* C
	* Arduino
	* Python

ไลบรารี่ที่ใช้ในการพัฒนา
	* pyusb
	* pygame

รายละเอียดไฟล์ที่เกี่ยวข้อง

1. ไฟล์ตัวเกม
	* main.py เป็นไฟล์หลักสำหรับรันเกม
	* player.py เป็นไฟล์ที่เก็บคลาสและฟังก์ชันที่เกี่ยวข้องกับผู้เล่น
	* bear.py เป็นไฟล์ที่เก็บคลาสและฟังก์ชันที่เกี่ยวข้องกับหมี
	* arrow.py เป็นไฟล์ที่เก็บคลาสและฟังก์ชันที่เกี่ยวข้องกับลูกธนู
	* gamemap.py เป็นไฟล์ที่เก็บคลาสและฟังก์ชันที่เกี่ยวข้องกับแผนที่

2. ไฟล์ที่เกี่ยวข้องกับการติดต่อกับบอร์ดไมโครคอนโทรลเลอร์
	* peri.py 
	* practicum.py
	* usb-generic/usb-generic.ino
	* usb-generic/usbconfig.ino

3. ไฟล์รูปภาพและเสียงประกอบ
	* src/images/
	* src/sounds/

4. ไฟล์ที่เกี่ยวกับ schematic
	* schematic/

ฮาร์ดแวร์ที่ใช้
	* Practicum Board
	* PCB board
	* LDR * 3
	* LED * 3
	* Switch * 1
	* Header 40 pin
	* Sound Sensor
	
License
Let's hunt the little bears project is freely distributable under the terms of the MIT license.
	
-------------------------------------------------------------------------------------------------------

Project name: Let's hunt the little bears!

Team name: สามเกลอเจอหมี
Member:
	1. 5710500178 Jenwich Rattanayenjai
	2. 5710503444 Booranasit Piyavatcharavijit
	3. 5710503487 Panupong Maneerut
Practicum for Computer Engineering, Department of Computer Engineering, Faculty of Engineering, Kasetsart University

Description:
This game is about hunting the bears. We can control the archer to move left or right. We can adjust force and angle of arrow. And we also blow the sound censor on the board to clear all bears when it ready.

Language used in this project
	* C
	* Arduino
	* Python

Library used in this project
	* pyusb
	* pygame

Detail about files
1. Game files
	* main.py - main file for run the game
	* player.py - contains class and function about player
	* bear.py - contains class and function about bear
	* arrow.py - contains class and function about arrow
	* gamemap.py - contains class and function about map

2. Files about communicate to micro-controller board
	* peri.py 
	* practicum.py
	* usb-generic/usb-generic.ino
	* usb-generic/usbconfig.ino

3. Images and sound
	* src/images/
	* src/sounds/

4. Files about schematic
	* schematic/

Hardware
	* Practicum Board
	* PCB board
	* LDR * 3
	* LED * 3
	* Switch * 1
	* Header 40 pin
	* Sound Sensor
	
License
Let's hunt the little bears project is freely distributable under the terms of the MIT license.
