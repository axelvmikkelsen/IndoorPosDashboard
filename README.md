# IndoorPosDashboard

This application is based on the [Pozyx Positioning System](https://www.pozyx.io/), aiming to use positioning data to visualize and analyze flow of items in a production/inventory system.

The Pozyx software is limited to real-time view of a constructed "digital twin", below is a to scale version of a test-lab at NTNU with active tags seen in blue.

![Pozyx](https://user-images.githubusercontent.com/52491186/65998541-c6ed1200-e49b-11e9-80e7-1cc19b8db12a.PNG)

Connection to the Pozyx Server is established thorugh `view_content\connect.py`.

The Django/Python application is currently able to connect and retireve live tag data.

![DashRec](https://user-images.githubusercontent.com/52491186/65997733-34983e80-e49a-11e9-9fb7-8a9283ed46e7.gif)

This project is still in progress, so a internet-based version is not supported yet.
