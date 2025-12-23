Air Tracker: Technical Project Documentation
1. Project Overview 
● Name: Air Tracker Flight Analysis Project 
● Role: An end-to-end data engineering and analytics pipeline for global aviation monitoring. 
● Core Stack: Engineered using Python, SQLite, Pandas, and Streamlit. 
● Objective: To architect a system that ingests high-velocity flight data, maintains a relational schema, and generates operational intelligence via a custom dashboard.

2. Core Functionalities 
● Automated Ingestion: Synchronizes data across Airport, Flight, and Aircraft entities using REST APIs. 
● Data Persistence: Implements a robust ETL process to clean and store unstructured API responses into a normalized SQLite database. 
● Operational Analytics: Leverages complex SQL logic to extract insights on fleet utilization and global air traffic. 
● Interactive UI: A multi-page Streamlit application designed for real-time data exploration and filtering. 
● Resource Management: Utilizes a custom JSON caching layer to optimize API consumption and ensure performance stability.

3. Streamlit Application Features  
● Executive Dashboard: Visualizes high-level KPIs including total fleet activity, airport throughput, and global delay trends.  
● Advanced Search Engine: Granular filtering capabilities by flight identifier, airline carrier, and temporal ranges. 
● Geospatial Insights: Comprehensive airport profiles featuring UTC offsets, geographic coordinates, and inbound/outbound flow logs. 
● Performance Analytics: Quantitative comparison of arrival versus departure delay vectors using statistical aggregations. 
● Intelligent Logic Layer: Automated categorization of flight sectors (Domestic vs. International) and identification of high-traffic corridors.

4. Data Engineering & SQL Logic 
● Schema Design: Orchestrated a relational database model to maintain referential integrity between aircraft and flight schedules. 
● Advanced Aggregations: Developed queries to track flight frequency per aircraft model and detect scheduling overlaps. 
● Conditional Analysis: Implemented CASE WHEN logic for real-time flight status monitoring (Scheduled, Departed, Cancelled). 
● Fleet Utilization: Evaluates route diversity and aircraft deployment patterns across various airline networks.

5. Implementation & Execution 
● Step 1: Environment setup and dependency management via pip install -r requirements.txt. 
● Step 2: Database initialization through sequential execution of modular API scripts. 
● Step 3: Deployment of the analytical engine using streamlit run streamlit_app/app.py.

6. Project Impact & Outcomes 
● Full-Stack Proficiency: Demonstrates a complete handle on the data lifecycle from raw extraction to stakeholder visualization. 
● Production-Ready Logic: Showcases the ability to handle rate-limited external APIs and complex relational data structures. 
● Modular Architecture: The project is designed with a strict separation between the data backend and the visualization frontend.