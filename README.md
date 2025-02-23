# QuarGen CLI

QuarGen is a command-line tool developed for the QuarTrend project.
Its purpose is to automate the generation of a standardized modular structure for applications,
enabling quick and consistent module generation for both development and production environments.

---

## Main Features

- **Complete Modular Structure Generation**
  - **Base Directories and Files:**
    - `config/`: Contains the `default.py` file with configurations (e.g., API port, UI theme, socket enablement).
    - `docs/`: Includes documentation files such as `installation.md` and `usage.md`.
    - `models/`: Divided into:
      - `domain/`: For business models.
      - `dto/`: For Data Transfer Objects.
    - `controllers/`: Divided into:
      - `rest/`: For REST API controllers.
      - `web/`: For web controllers (if needed).
    - `services/`: Divided into:
      - `business/`: For business logic.
      - `data/`: For data access.
    - `utils/`: Contains utilities such as the `ColoredLogger` class for colored logging.
    - `tests/`: For unit and integration tests.
    - `api/`: Implements the API module using Flask blueprints.
      - **Automatic Registration of Endpoints:**  
        The system recursively scans the `api/` folder (including `api/endpoints/`) to register extra endpoints,
        ensuring each blueprint is uniquely named to avoid conflicts.
    - `ui/`: Includes:
      - `templates/`: Organized in subdirectories like `html_templates/` (with `base/ui_base_template.html` and `ui_index_template.html`).
      - `static/`: With subfolders for `css/`, `js/`, and `images/`.
      - `endpoints/`: A separate folder (outside `templates/`) for extra UI endpoints.
    - `sockets/`: For managing socket connections.
    - `interfaces/`: Defines the base interfaces (core, data, config, business) to be implemented by all components.
    - `main.py`: The application entry point that automatically registers API, UI, sockets, controllers, and extra endpoints.
    - `webpack.config.js` and `package.json`: For building the front-end via webpack.
    - Additional files: `.env`, `README.md`, `requirements.txt`, and the `module_manifest.json` file describing the module.

- **Unique Blueprint Names for Controllers and Endpoints**
  - To prevent conflicts during automatic blueprint registration, blueprint names are now generated uniquely
    by concatenating the module name with the lower-case component class name and an appropriate suffix (e.g., `_controller` or `_endpoint`).
  - This change ensures that even if multiple controllers or endpoints are added, each blueprint will have a unique name.

- **CLI Commands**
  - **generate:** Generates the entire structure of a new module.  
    Adding the `main` flag sets the module as the main one (with `/` endpoint).
  - **dev:** Starts the application in development mode by running `main.py` as a module, ensuring correct relative imports.
  - **build:** Performs the production build using webpack to bundle and minify JavaScript files.
  - **add:** Allows you to add new components such as controllers, services, models, templates, endpoints, and database modules.
    - For **controllers**, you can specify a subtype (`rest` or `web`).
    - For **services**, the subtype can be `business` or `data`.
    - For **models**, the subtype can be `domain` or `dto`.
    - For **templates**, if the `--url_prefix` option is provided, an extra endpoint is generated in the `ui/endpoints` folder.
    - For **extra API endpoints**, the `--prefix` flag is used to specify the route, and the blueprint is named uniquely.
    
    Example:
    ```bash
    python -m cli.quargen add controller UserController MyApp "/users/<id_user>/profile"
    python -m cli.quargen add endpoint ExtraAPI MyApp --prefix extra
    ```

- **Colored Logger**
  - The `ColoredLogger` class provides colored log output based on the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL),
    which simplifies debugging and monitoring.

- **Automatic Component Registration**
  - The generated `main.py`:
    - Imports and initializes the API, UI, and Sockets modules.
    - Automatically registers all controllers in the `controllers` folder through recursive scanning.
    - Automatically registers extra API endpoints from the `api/` folder, ensuring that each blueprint is registered only once using unique names.

- **Template Organization**
  - HTML templates for the UI are managed in the `templates/html_templates/` folder:
    - `base/ui_base_template.html`: The base template.
    - `ui_index_template.html`: The index page template.
  - The Python template for the main entry point is located in `templates/py_templates/main_template.py`.

- **Module Manifest**
  - Each generated module includes a `module_manifest.json` file containing metadata about the module,
    which is useful for aggregating modules and future operations.

---

## How QuarGen Works

1. **Module Generation**
   - Run the command:
     ```bash
     python quargen.py generate --name MyApp --base <path>
     ```
   - A complete modular structure is created with all necessary directories and files,
     including `__init__.py` files to designate Python packages and the manifest file.

2. **Development Mode**
   - Start the application with:
     ```bash
     python quargen.py dev --module MyApp
     ```
   - The DevServer changes the working directory to the parent of `MyApp` and launches the app as a module
     (`python -m MyApp.main`), ensuring that relative imports are correctly resolved.
   - The `main.py` file automatically registers API, UI, Sockets, all controllers, and extra endpoints.

3. **Production Build**
   - Run the command:
     ```bash
     python quargen.py build --module MyApp
     ```
   - This command executes `npm install` and `npx webpack` to generate a production-ready bundle of the JS files.

4. **Adding New Components**
   - Use the `add` command to add new components. For example:
     - **UI Template with Extra Endpoint:**
       ```bash
       python quargen.py add template CustomTemplate MyApp --url_prefix custom
       ```
     - **Extra API Endpoint:**
       ```bash
       python -m cli.quargen add endpoint ExtraAPI MyApp --prefix extra
       ```
     - Similarly, you can add controllers, services, and models by specifying the appropriate subtype (e.g., `rest`, `business`, `domain`, etc.).

5. **Colored Logger**
   - During execution, the `ColoredLogger` produces colored log output in the console, facilitating easier debugging.

---

## What the Software Does

- **Automates the Generation of a Modular Structure:**  
  It creates a complete module for QuarTrend in a standardized way,
  including all necessary components for API, UI, sockets, and business logic.

- **Simplifies Startup and Build Management:**  
  Provides commands to start the app in development mode and to build the module for production using webpack.

- **Extensibility and Aggregation:**  
  All components implement standard interfaces, allowing automatic aggregation of logic from different modules into a cohesive project.

- **Unique Blueprint Registration:**  
  The system now generates unique blueprint names by incorporating both the module and component names,
  preventing registration conflicts during automatic blueprint imports.

- **Centralized Template Management:**  
  UI and main templates are managed in specific folders for easier maintenance.

- **Module Manifest:**  
  Each module generates a `module_manifest.json` file with module information, aiding in future module aggregation operations.

---

## Future Developments

- **Enhanced Testing and CI/CD:**
  - Expand unit and integration tests.
  - Integrate Continuous Integration tools for automatic testing and deployment.

- **Improved Documentation and Logging:**
  - Further refine internal and external documentation.
  - Enhance logging messages for even more intuitive debugging.

- **Extended Component Support:**
  - Introduce additional component types and customization options.
  - Explore support for other languages or frameworks in the module generation process.

- **Optimized Build and Deployment:**
  - Incorporate advanced tools for bundling and minification.
  - Automate deployment to staging and production environments.

---

## How to Contribute

If you wish to contribute to QuarGen, fork the repository, make your changes, and open a pull request.
Refer to the `CONTRIBUTING.md` file for guidelines on contributing.

---

With QuarGen, you can rapidly generate a standardized and scalable modular structure,
greatly simplifying development and integration of applications for the QuarTrend project.
