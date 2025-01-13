# Property Finder

Property Finder is an application designed to simplify the process of registering properties and agents, associating agents with
properties, and enabling users to find their ideal property using powerful search capabilities. The application leverages
Elasticsearch for fast and accurate search results, ensuring users can easily discover properties that match their needs.

---

## Features

- **Property and Agent Management**: Register properties and agents and associate them seamlessly.
- **Advanced Search Engine**: Powered by Elasticsearch to deliver precise and relevant results.
- **Clean Architecture**: A layered structure implementing common patterns like Repository, Service Layer, and Dependency Injection.
- **Asynchronous Processing**: Utilizes Celery and Redis for non-blocking background tasks.
- **Message Broker Integration**: Uses Kafka for publishing domain events.
- **PostgreSQL and PgBouncer**: Ensures reliable data persistence and connection pooling.
- **RESTful APIs**: Provides a user-friendly interface for interacting with the application.

---

## Technologies Used

- **Python**: Version 3.13.
- **Django**: Web framework for the presentation layer.
- **Elasticsearch**: For indexing and searching data.
- **PostgreSQL**: Relational database serving as the source of truth.
- **Kafka**: Message broker for domain events handling.
- **Celery**: Task queue for asynchronous operations.
- **Redis**: Backend for Celery task processing.
- **PgBouncer**: Connection pooling for PostgreSQL.

---

## Architecture

This application follows the principles of Clean Architecture with the following layers:

1. **Presentation Layer**:
    - Responsible for handling API requests and responses.
    - Includes serializers for data validation and transformation.

2. **Use Case Layer**:
    - Encapsulates specific business use cases.
    - Isolated from the presentation layer, ensuring modularity and maintainability.

3. **Service Layer**:
    - Contains business logic and coordinates data retrieval and manipulation.
    - Interacts with repositories to ensure data consistency across PostgreSQL and Elasticsearch.

4. **Repository Layer**:
    - Handles data persistence and retrieval.
    - Implements the Repository pattern to abstract data access.

### Why Use the Repository Pattern?

The Repository pattern centralizes data access logic, making it easier to:

- Swap or extend data sources (e.g., switch from PostgreSQL to another database).
- Maintain consistency between multiple data sources (e.g., PostgreSQL and Elasticsearch).

---

## Installation

### Prerequisites

- **Docker**: For running services like PostgreSQL, Elasticsearch, Kafka, and Redis.

---

## Running the Application

1. **Start Required Services**:
   Use Docker compose to build and start services:
   ```bash
   docker-compose build
   ```

2. **Run application**
   You can run application by docker compose:
   ```bash
   docker compose up
   ```

---

# Explanation of Property Service [As Service layer Example]

This implementation demonstrates the business logic from interacting with repositories to running asynchronous processes using Celery
for non-blocking operations such as updating or deleting data. It ensures data consistency between PostgreSQL and Elasticsearch.
PostgreSQL serves as the source of truth, while Elasticsearch provides search capabilities.

## Overview

The `PropertyService` ensures that data consistency rules between PostgreSQL and Elasticsearch are maintained. Here's how it handles
creating, updating, and deleting properties in the system:

### Key Processes

1. **Creating a Property**:
    - When a property is created, it is inserted into both PostgreSQL and Elasticsearch simultaneously to maintain consistency from
      the start.
    - Example:
        - Data is first saved in PostgreSQL.
        - The created instance is indexed in Elasticsearch.
        - An email notification is sent asynchronously using Kafka and Celery.

2. **Updating a Property**:
    - Related information like main type, sub type, and agent type is retrieved from PostgreSQL to ensure data consistency.
    - The property is updated in Elasticsearch first to ensure search results are accurate and up-to-date.
    - The synchronization with PostgreSQL happens asynchronously to maintain performance.

3. **Deleting a Property**:
    - The property is deleted from Elasticsearch first, ensuring it is no longer visible to users.
    - The deletion in PostgreSQL occurs asynchronously to ensure eventual consistency.

### Why Elasticsearch is Updated First

Updating Elasticsearch first ensures that users experience the most up-to-date information when searching through properties.
Synchronization with PostgreSQL happens asynchronously, maintaining system performance and consistency.

## Class: `PropertyService`

### Purpose

The `PropertyService` implements the business logic between the presentation layer and the domain layer. It interacts with:

- `PropertyDjangoRepository` (PostgreSQL repository)
- `PropertyElasticSearchRepository` (Elasticsearch repository)
- `AgentDjangoRepository`
- `PropertyTypeRepository`

### Methods

#### `create_property(main_type, sub_type, title, description, agent) -> Property`

Creates a new property in both PostgreSQL and Elasticsearch and sends an email notification.

#### `find_property(pk: int) -> Property`

Retrieves a property instance from PostgreSQL by its primary key.

#### `_prepare_update_dict(updates: Dict[str, Any]) -> Dict[str, Any]`

Prepares a dictionary of updates for Elasticsearch, ensuring consistency with PostgreSQL data.

#### `update_property(pk: int, updates: Dict[str, Any]) -> Dict[str, Any]`

Updates a property in Elasticsearch first and then synchronizes the changes to PostgreSQL asynchronously.

#### `delete_property(pk: int)`

Deletes a property from Elasticsearch first and then removes it from PostgreSQL asynchronously.

#### `search_property(query: str, **kwargs) -> List[Dict[str, Any]]`

Searches properties in Elasticsearch based on the given query.

#### `get_property_types()`

Retrieves all property types from PostgreSQL.

## Dependencies

- **PostgreSQL**: Source of truth for property information.
- **Elasticsearch**: Provides search capabilities for properties.
- **Kafka**: Used for event logging and messaging.
- **Celery**: Handles asynchronous tasks for non-blocking operations.

## Key Features

- Maintains data consistency between PostgreSQL and Elasticsearch.
- Uses asynchronous operations for better performance.
- Supports search functionality using Elasticsearch.
- Handles updates and deletions efficiently with minimal downtime for users.

## API Collection Documentation

You can access API swagger UI by opening ```localhost``` in your browser, or accessing below postman collection.

https://www.postman.com/aliseylaneh/ali-seylaneh/collection/u6759hu/property-finder-api?action=share&creator=32296300