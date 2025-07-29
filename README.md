<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">

<!-- <img src="readmeai/assets/logos/purple.svg" width="30%" style="position: relative; top: 0; right: 0;" alt="Project Logo"/> -->

# SQES_API

<em></em>

<!-- BADGES -->
<!-- local repository, no metadata badges. -->

<em>Built with the tools and technologies:</em>

<img src="https://img.shields.io/badge/Typer-000000.svg?style=default&logo=Typer&logoColor=white" alt="Typer">
<img src="https://img.shields.io/badge/SQLAlchemy-D71F00.svg?style=default&logo=SQLAlchemy&logoColor=white" alt="SQLAlchemy">
<img src="https://img.shields.io/badge/Rich-FAE742.svg?style=default&logo=Rich&logoColor=black" alt="Rich">
<img src="https://img.shields.io/badge/Gunicorn-499848.svg?style=default&logo=Gunicorn&logoColor=white" alt="Gunicorn">
<img src="https://img.shields.io/badge/FastAPI-009688.svg?style=default&logo=FastAPI&logoColor=white" alt="FastAPI">
<br>
<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=default&logo=Docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=default&logo=Python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Google%20Cloud%20Storage-AECBFA.svg?style=default&logo=Google-Cloud-Storage&logoColor=black" alt="Google%20Cloud%20Storage">
<img src="https://img.shields.io/badge/Pydantic-E92063.svg?style=default&logo=Pydantic&logoColor=white" alt="Pydantic">
<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=default&logo=YAML&logoColor=white" alt="YAML">

</div>
<br>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
    - [Project Index](#project-index)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview



---

## Features

<code>❯ REPLACE-ME</code>

---

## Project Structure

```sh
└── sqes_api/
    ├── Dockerfile
    ├── __pycache__
    │   └── main.cpython-312.pyc
    ├── compose.yaml
    ├── nginx.conf
    ├── requirements.txt
    └── src
        ├── __init__.py
        ├── __pycache__
        ├── auth
        ├── core
        ├── main.py
        ├── modules
        └── schemas.py
```

### Project Index

<details open>
	<summary><b><code>SQES_API/</code></b></summary>
	<!-- __root__ Submodule -->
	<details>
		<summary><b>__root__</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ __root__</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/requirements.txt'>requirements.txt</a></b></td>
					<td style='padding: 8px;'>- Requirements.txt specifies the projects dependencies<br>- It lists numerous packages, including FastAPI for the web framework, Firebase Admin for cloud integration, SQLAlchemy for database interaction, and various other libraries for networking, data handling, and development tools<br>- The file ensures all necessary components are installed for successful project execution.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/nginx.conf'>nginx.conf</a></b></td>
					<td style='padding: 8px;'>- Nginx acts as a reverse proxy, routing external requests to an internal FastAPI application<br>- It listens on port 2107, forwarding traffic to the FastAPI server running on port 8000 within a Docker container named <code>fastapi_app</code><br>- Essential headers are passed to ensure correct request information reaches the FastAPI application, enabling seamless communication between the external network and the internal application server.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/compose.yaml'>compose.yaml</a></b></td>
					<td style='padding: 8px;'>- A FastAPI application and an Nginx reverse proxy<br>- The FastAPI service utilizes environment variables, mounts sensitive data, and connects to a private network<br>- Nginx, dependent on the FastAPI service, exposes the application via port 2107<br>- A custom network facilitates secure inter-container communication.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/Dockerfile'>Dockerfile</a></b></td>
					<td style='padding: 8px;'>- The Dockerfile constructs a production-ready container image<br>- It leverages a multi-stage build for efficiency, installing dependencies and creating a secure, non-root user environment<br>- The image runs a Python application using Uvicorn, configured to listen on port 8000 for connections from a reverse proxy like Nginx<br>- The process optimizes security and performance for deployment.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- src Submodule -->
	<details>
		<summary><b>src</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ src</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/schemas.py'>schemas.py</a></b></td>
					<td style='padding: 8px;'>- Src/schemas.py` defines Pydantic models for structuring API responses<br>- These models ensure consistent data formats for the root endpoint and various API modules (authentication, metadata, quality control, health)<br>- The models facilitate predictable responses, including service information, status, and links to documentation and individual modules, thereby improving API usability and maintainability.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/main.py'>main.py</a></b></td>
					<td style='padding: 8px;'>- The main.py file constitutes the FastAPI applications entry point, initializing core services and configuring middleware<br>- It establishes database connections (MySQL and PostgreSQL), initializes Firebase, and mounts various API modules (authentication, metadata, quality control, and health checks)<br>- The application includes CORS middleware and custom logging for enhanced security and monitoring<br>- A root endpoint provides service status and links to other API sections.</td>
				</tr>
			</table>
			<!-- core Submodule -->
			<details>
				<summary><b>core</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ src.core</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/core/database.py'>database.py</a></b></td>
							<td style='padding: 8px;'>- The <code>database.py</code> module establishes connections to both MySQL and PostgreSQL databases<br>- It leverages configuration settings to define connection parameters and creates SQLAlchemy engine and session objects for each database<br>- This facilitates database interactions throughout the application, providing a consistent interface for data access.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/core/firebase.py'>firebase.py</a></b></td>
							<td style='padding: 8px;'>- The <code>firebase.py</code> module provides a function to initialize the Firebase Admin SDK<br>- It ensures the SDK is initialized only once, using a provided service account key path<br>- Robust error handling prevents application startup if the key path is invalid or the file is missing<br>- Successful initialization logs a confirmation message; otherwise, detailed error logging facilitates debugging<br>- This module integrates Firebase authentication and other services into the application.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/core/dependencies.py'>dependencies.py</a></b></td>
							<td style='padding: 8px;'>- Dependencies.py` provides database session management for the application<br>- It defines functions to obtain and automatically close SQLAlchemy sessions for both MySQL and PostgreSQL databases<br>- These functions, exposed as dependencies, streamline database interaction within FastAPI endpoints, ensuring efficient resource management and cleaner endpoint definitions.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/core/config.py'>config.py</a></b></td>
							<td style='padding: 8px;'>- The <code>config.py</code> module centralizes application settings for the SQES Data API<br>- It uses Pydantic to manage configuration parameters, loading them from environment variables or a <code>.env</code> file<br>- These settings encompass core application details, API documentation options, security configurations, database connection strings, Firebase credentials, feature-specific parameters, and debugging options<br>- Environment-specific overrides ensure production deployments prioritize security and performance.</td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- auth Submodule -->
			<details>
				<summary><b>auth</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ src.auth</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/auth/routing.py'>routing.py</a></b></td>
							<td style='padding: 8px;'>- The <code>routing.py</code> module defines FastAPI routes for authentication within a larger application<br>- It provides endpoints to retrieve authenticated user information and to manage user roles, specifically setting custom claims<br>- These functionalities leverage Firebase Admin SDK for authentication and authorization, ensuring secure access control<br>- Robust logging is implemented for auditing and debugging purposes.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/auth/dependencies.py'>dependencies.py</a></b></td>
							<td style='padding: 8px;'>- Authentication dependencies manage user access control<br>- It verifies Firebase ID tokens, retrieves user details from Firestore, and enforces authorization based on predefined scopes and roles<br>- A debug bypass mechanism is included for development<br>- The module provides reusable dependency functions for common authorization checks, simplifying endpoint security implementation.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/auth/schemas.py'>schemas.py</a></b></td>
							<td style='padding: 8px;'>- Src/auth/schemas.py<code> defines the </code>FirebaseUser` Pydantic model<br>- It structures user data, integrating Firebase authentication claims with Firestore profile information<br>- The model encompasses user identification, authentication status, roles, permissions, and timestamps<br>- It facilitates data validation and consistent user representation within the authentication system.</td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- modules Submodule -->
			<details>
				<summary><b>modules</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ src.modules</b></code>
					<!-- qualitycontrol Submodule -->
					<details>
						<summary><b>qualitycontrol</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ src.modules.qualitycontrol</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/modules/qualitycontrol/models.py'>models.py</a></b></td>
									<td style='padding: 8px;'>- The <code>models.py</code> file defines SQLAlchemy models for storing station data quality information within the quality control module<br>- It creates PostgreSQL database tables representing station quality metrics, including overall quality assessments and detailed QC results per channel<br>- These models facilitate data persistence and retrieval, supporting the applications quality control functionalities<br>- Relationships between tables ensure data integrity and efficient querying.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/modules/qualitycontrol/routing.py'>routing.py</a></b></td>
									<td style='padding: 8px;'>- The <code>routing.py</code> module defines API endpoints for accessing quality control data<br>- It provides functionalities to retrieve daily quality summaries, detailed station data, yearly quality history, and station site information<br>- Additionally, it offers access to power spectral density and signal images<br>- All endpoints are secured using authentication, ensuring data access control<br>- The module integrates with database access and data service layers within the larger application.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/modules/qualitycontrol/schemas.py'>schemas.py</a></b></td>
									<td style='padding: 8px;'>- Schemas define data models for quality control (QC) results<br>- <code>QcResultSummaryResponseBase</code> provides summarized QC metrics and station metadata, while <code>StationsQCDetailsResponseBase</code> offers detailed QC metrics for individual channels<br>- These schemas facilitate data exchange within the quality control module and likely serve as interfaces for API responses<br>- Geographic coordinates are represented using a <code>GeometryBase</code> schema.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/modules/qualitycontrol/services.py'>services.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- health Submodule -->
					<details>
						<summary><b>health</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ src.modules.health</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/modules/health/routing.py'>routing.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- metadata Submodule -->
					<details>
						<summary><b>metadata</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ src.modules.metadata</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/modules/metadata/models.py'>models.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/modules/metadata/routing.py'>routing.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/modules/metadata/schemas.py'>schemas.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='/home/geo2sqes/putu_dev/sqes_api/blob/master/src/modules/metadata/services.py'>services.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
</details>

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python
- **Package Manager:** Pip
- **Container Runtime:** Docker

### Installation

Build sqes_api from the source and intsall dependencies:

1. **Clone the repository:**

    ```sh
    ❯ git clone ../sqes_api
    ```

2. **Navigate to the project directory:**

    ```sh
    ❯ cd sqes_api
    ```

3. **Install the dependencies:**

<!-- SHIELDS BADGE CURRENTLY DISABLED -->
	<!-- [![docker][docker-shield]][docker-link] -->
	<!-- REFERENCE LINKS -->
	<!-- [docker-shield]: https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white -->
	<!-- [docker-link]: https://www.docker.com/ -->

	**Using [docker](https://www.docker.com/):**

	```sh
	❯ docker build -t putu_dev/sqes_api .
	```
<!-- SHIELDS BADGE CURRENTLY DISABLED -->
	<!-- [![pip][pip-shield]][pip-link] -->
	<!-- REFERENCE LINKS -->
	<!-- [pip-shield]: https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white -->
	<!-- [pip-link]: https://pypi.org/project/pip/ -->

	**Using [pip](https://pypi.org/project/pip/):**

	```sh
	❯ pip install -r requirements.txt
	```

### Usage

Run the project with:

**Using [docker](https://www.docker.com/):**
```sh
docker run -it {image_name}
```
**Using [pip](https://pypi.org/project/pip/):**
```sh
python {entrypoint}
```

### Testing

Sqes_api uses the {__test_framework__} test framework. Run the test suite with:

**Using [pip](https://pypi.org/project/pip/):**
```sh
pytest
```

---

## Roadmap

- [X] **`Task 1`**: <strike>Implement feature one.</strike>
- [ ] **`Task 2`**: Implement feature two.
- [ ] **`Task 3`**: Implement feature three.

---

## Contributing

- **💬 [Join the Discussions](https://LOCAL/putu_dev/sqes_api/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://LOCAL/putu_dev/sqes_api/issues)**: Submit bugs found or log feature requests for the `sqes_api` project.
- **💡 [Submit Pull Requests](https://LOCAL/putu_dev/sqes_api/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your LOCAL account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone /home/geo2sqes/putu_dev/sqes_api
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to LOCAL**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://LOCAL{/putu_dev/sqes_api/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=putu_dev/sqes_api">
   </a>
</p>
</details>

---

## License

Sqes_api is protected under the [LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

## Acknowledgments

- Credit `contributors`, `inspiration`, `references`, etc.

<div align="right">

[![][back-to-top]](#top)

</div>


[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square


---
