import MySQLdb
import folium
import csv
import mysql_connect

with open('./i-touch_update.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    update_dates = {rows[0]:rows[1] for rows in reader}

db = MySQLdb.connect(host=mysql_connect.ip,
                     user=mysql_connect.account,
                     passwd=mysql_connect.password,
                     charset="utf8")
cursor = db.cursor()

cursor.execute('USE EEW')
cursor.execute("SELECT l.locname, \
                   l.station, \
                   l.serial, \
                   l.longitude, \
                   l.latitude, \
                   s.statusflag, \
                   d.floor, \
                   d.room, \
                   d.contact, \
                   d.phone \
               FROM PalertList AS l \
                   INNER JOIN PalertStatus AS s \
                       ON l.station = s.station \
                   INNER JOIN PalertDetailLocation AS d \
                       ON l.station = d.station \
               ")

m = folium.Map(location=[23.974896, 120.979649],
               zoom_start=8)

feature_group1 = folium.FeatureGroup(name='好新')
feature_group2 = folium.FeatureGroup(name='壞新')
feature_group3 = folium.FeatureGroup(name='好舊')
feature_group4 = folium.FeatureGroup(name='壞舊')

locname, station, serial, longitude, latitude, statusflag, floor, room, contact, phone = cursor.fetchone()
while (True):
    url = "https://www.google.com.tw/maps/search/" + locname + "/@" + str(latitude) + "," + str(longitude) + ",18z"
    
    try:        
        html = ("<b>" + locname + "</b><br>" + 
                "站碼：" + station + "<br>" +
                "序號：" + str(serial) + "<br>" +
                "硬體更新時間：<br>" + update_dates[station] + "<br>"
                "樓層：" + str(floor) + "<br>" +
                "房間：" + str(room) + "<br>" +
                "聯絡人：" + str(contact) + "<br>" +
                "電話：" + str(phone) + "<br>" +
                "<a href='" + 
		url + 
		"' target='blank'>地點</a><br>")
        if statusflag == 7 or statusflag == 3:
            folium.Marker(location = [latitude, longitude],
                          popup = html,
                          tooltip = locname,
                          icon=folium.Icon(icon="check", prefix='fa', color = 'green')
                         ).add_to(feature_group1)
        else:
            folium.Marker(location = [latitude, longitude],
                          popup = html,
                          tooltip = locname,
                          icon=folium.Icon(icon='check', prefix='fa', color = 'red')
                         ).add_to(feature_group2)
        
    except:
        html = ("<b>" + locname + "</b><br>" + 
                "站碼：" + station + "<br>" +
                "序號：" + str(serial) + "<br>" +
                "硬體未更新<br>"+
                "樓層：" + str(floor) + "<br>" +
                "房間：" + str(room) + "<br>" +
                "聯絡人：" + str(contact) + "<br>" +
                "電話：" + str(phone) + "<br>" +
                "<a href='" + 
		url + 
		"' target='blank'>地點</a><br>")
        if statusflag == 7 or statusflag == 3:
            folium.Marker(location = [latitude, longitude],
                          popup = html,
                          tooltip = locname,
                          icon=folium.Icon(icon="times", icon_color="black", prefix='fa', color = 'green')
                         ).add_to(feature_group3)
        else:
            folium.Marker(location = [latitude, longitude],
                          popup = html,
                          tooltip = locname,
                          icon=folium.Icon(icon='times', icon_color="black", prefix='fa', color = 'red')
                         ).add_to(feature_group4)
    try:
        locname, station, serial, longitude, latitude, statusflag, floor, room, contact, phone = cursor.fetchone()
    except:
        break
                
feature_group1.add_to(m)
feature_group2.add_to(m)
feature_group3.add_to(m)
feature_group4.add_to(m)
folium.LayerControl().add_to(m)
m.save('/var/www/html/test3.html')

cursor.close()
db.close()
