#include <SPI.h>
#include <Dhcp.h>
#include <ethernet_comp.h>
#include <UIPClient.h>
#include <UIPEthernet.h>
#include <UIPServer.h>
#include <DHT.h>
#define DHTPIN A0
#define DHTTYPE DHT22  
DHT dht(DHTPIN, DHTTYPE);
 
byte mac[] = {0x74,0x69,0x69,0x2D,0x30,0x31};
EthernetServer server(80);
 
void setup() {
  Serial.begin(9600);
  Ethernet.begin(mac);
  server.begin();
  dht.begin();
}
 
void loop() {
  delay(100);
  // listen for incoming clients
  EthernetClient client = server.available();
  if (client) {
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        // if you've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so you can send a reply
        if (c == '\n' && currentLineIsBlank) 
        {
           // send a standard http response header
           client.println("HTTP/1.1 200 OK");
           client.println("Content-Type: text/html");
           client.println("Connection: close");  // the connection will be closed after completion of the response
           client.println("Refresh: 1");  // refresh the page automatically every 5 sec
           client.println();
           client.println("<!DOCTYPE HTML>");
           client.println("<html>");
           // output the value of each analog input pin
           client.println("<head>");
           client.println("</head>");
           client.println("<body>");
 
           float h=dht.readHumidity();
           float t=dht.readTemperature();  
           if(isnan(h) || isnan(t))
           {
             client.println("Error! No Temperature and Humidity!");
             client.println("<br />");
             return;
           } 
           for(int m = 0 ; m < 1 ; ++m)
           { 
             h=dht.readHumidity();
             t=dht.readTemperature();
             client.print("Humidity:");
             client.print(h);
             client.print("Temperture:");
             client.print(t);
             client.println("<br />");
             if(t > 50.00 || h > 70.00)
             {
            // 普通报警声
                for(int i=0;i<160;i++)//输出一个频率的声音
                {
                  pinMode(4,OUTPUT);
                  digitalWrite(4,LOW);//发声音
                  delay(2);//延时2ms
                  digitalWrite(4,HIGH);//不发声音
                  delay(2);//延时2ms
                }
             }
             else
             {
            //   noTone(4);
                 digitalWrite(4,HIGH);//不发声音
             }  
             //delay(500);
           }
           client.println("<br />");
           client.println("<br />");
           client.println("</body>");
           client.println("</html>");
           break;
        }
        if (c == '\n') {
          // you're starting a new line
          currentLineIsBlank = true;
        } 
        else if (c != '\r') {
          // you've gotten a character on the current line
          currentLineIsBlank = false;
        }
      }
    }
    // give the web browser time to receive the data
    delay(1);
    // close the connection:
    client.stop();
  }
}

