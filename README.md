# Airport Runway Management System

A Python-based **Airport Runway Management System** developed as a Data Structures project. The system manages aircraft registration, landing and takeoff queues, flight searching, and departed flight history using fundamental data structures.

## Features

* Register new flights
* Search flights using flight number
* Manage **Landing Queue**
* Manage **Takeoff Queue**
* Process aircraft landing and takeoff
* Maintain departed flight history
* Display active flights and their current status
* GUI built using Python Tkinter
* Hash table collision handling using **Linear Probing**

## Data Structures Used

### 1. Queue — FIFO

Queues are used to manage aircraft waiting for runway operations.

* **Landing Queue** — aircraft waiting to land
* **Takeoff Queue** — aircraft waiting to take off
* Follows **FIFO (First In, First Out)**

### 2. Hash Table — Linear Probing

The hash table stores active flight information and allows flights to be searched using their flight number.

* Custom hash function
* Collision handling using **Linear Probing**
* Supports insertion, searching, deletion, and display

### 3. Stack — LIFO

A stack is used to maintain the history of departed flights.

* New departed flights are pushed onto the stack
* Most recently departed flight appears first
* Follows **LIFO (Last In, First Out)**

## Flight Status Flow

```text
Registered
    ↓
Waiting for Landing
    ↓
Landed
    ↓
Waiting for Takeoff
    ↓
Departed
```

## Project Structure

```text
Airport-Runway-Management-System/
│
├── airport.py
├── app.py
└── README.md
```

### `airport.py`

Contains the core Data Structures and backend logic:

* `Plane`
* `Queue`
* `HashTable`
* `Stack`

### `app.py`

Contains the **Tkinter graphical user interface** and connects the GUI with the data structures.

## Technologies Used

* **Python**
* **Tkinter**
* Object-Oriented Programming
* Data Structures and Algorithms

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/kunalshinde-14/Airport-Runway-Management-System.git
```

### 2. Open the project folder

```bash
cd Airport-Runway-Management-System
```

### 3. Run the application

```bash
python app.py
```

## Example Flight Information

```text
Flight No. : AI101
Airline    : Air India
Route      : Mumbai → Delhi
Aircraft   : Airbus A320
Status     : Registered
```

## DSA Concepts Demonstrated

| Data Structure | Application             | Principle      |
| -------------- | ----------------------- | -------------- |
| Queue          | Landing & Takeoff       | FIFO           |
| Hash Table     | Flight Search           | Linear Probing |
| Stack          | Departed Flight History | LIFO           |

## Project Objective

The main objective of this project is to demonstrate the practical implementation of **Data Structures using Python** by applying Queue, Hash Table, and Stack concepts to an airport runway management scenario.

## Limitations

* The system does not use a database.
* Flight information is stored only while the program is running.
* It is a simulation and does not connect to real airport systems.
* Runway scheduling is simplified for educational purposes.

## Future Scope

The project can be extended with:

* Database storage
* Multiple runway management
* Priority-based aircraft scheduling
* User authentication
* Detailed flight reports
* Real-time airport data integration

## Author

**Kunal Shinde**

Data Structures Using Python — Semester 3
Mahatma Education Society's Pillai College of Arts, Commerce & Science, New Panvel.
