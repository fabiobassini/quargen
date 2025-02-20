# QuarGen CLI

QuarGen is a command-line tool developed for the QuarTrend project.
Its purpose is to automate the generation of the module structure (repository)
for the project, creating a standardized modular architecture that can be easily integrated into larger systems.

---

## Main Features

- **Complete Modular Structure Generation**
  - **Base Directories and Files:**
    - `config/`: contains the `default.py` file with configurations (e.g., API port, UI theme, socket enablement).
    - `docs/`: includes documentation with files such as `installation.md` and `usage.md`.
    - `models/`: divided into:
      - `domain/`: for business models.
      - `dto/`: for Data Transfer Objects.
    - `controllers/`: divided into:
      - `rest/`: for REST API controllers.
      - `web/`: for web controllers (if needed).
    - `services/`: divided into:
      - `business/`: for business logic.
      - `data/`: for data access.
    - `utils/`: contains utilities such as the `ColoredLogger` class for colored logging.
    - `tests/`: for unit and integration tests.
    - `api/`: implements the API module using Flask blueprints. **The system recursively scans the `api/` folder to automatically register extra endpoints (including those in the `api/endpoints/` subfolder) while avoiding duplications.**
    - `ui/`: includes:
      - `templates/`: with the new structure:
        - `html_templates/`: contains the `base/` folder (with `ui_base_template.html`) and the file `ui_index_template.html`.
      - `static/`: with subfolders for `css/`, `js/`, and `images/`.
      - `endpoints/`: a separate folder (outside of `templates/`) for extra UI endpoints.
    - `sockets/`: for managing socket connections.
    - `interfaces/`: defines the base interfaces (core, data, config, business) that must be implemented by all components.
    - `main.py`: the application entry point that automatically registers API, UI, sockets, controllers, and extra endpoints.
    - `webpack.config.js` and `package.json`: for building the front-end via webpack.
    - Additional files: `.env`, `README.md`, `requirements.txt`, and the `module_manifest.json` file describing the module.

- **CLI Commands**
  - **generate:** Generates the entire structure of a new module.  
    By adding the `--main` flag, you indicate that the module will be the main one (with `/` endpoint).
  - **dev:** Starts the application in development mode by running `main.py` as a module (with correct relative imports).
  - **build:** Performs the production build using webpack to minimize JavaScript files.
  - **add:** Allows you to add new classes or templates.  
    - For **controllers**, you can specify a subtype (`rest` or `web`).
    - For **services**, the subtype can be `business` or `data`.
    - For **models**, the subtype can be `domain` or `dto`.
    - For **templates**, if the `--url_prefix` option is provided, an extra endpoint is also generated in the `ui/endpoints` folder.
    - You can also add new **extra API endpoints** using the `--prefix` flag.

- **Colored Logger**
  - The `ColoredLogger` class provides colored logs based on the level (DEBUG, INFO, WARNING, ERROR, CRITICAL), making debugging easier.

- **Automatic Component Registration**
  - The generated `main.py`:
    - Imports and initializes the API, UI, and Sockets modules.
    - Automatically registers all controllers in the `controllers` folder (recursive scanning).
    - **Now also automatically registers extra API endpoints present in the `api/` folder (including those in `api/endpoints/`), ensuring that each blueprint is registered only once.**

- **Template Organization**
  - The HTML templates for the UI are now managed in the `templates/html_templates/` folder:
    - `base/ui_base_template.html`: the base template.
    - `ui_index_template.html`: the index page template.
  - The Python template for the main entry point is located in `templates/py_templates/main_template.py`.

- **Module Manifest**
  - Each generated module includes a `module_manifest.json` file containing information about the module,
    which is useful for future aggregation operations between repositories.

---

## How QuarGen Works

1. **Module Generation**
   - Run the command:
     ```bash
     python quargen.py generate --name MyApp --base <path>
     ```
   - A complete modular structure is created with all necessary directories and files,
     including `__init__.py` files to make each folder a Python package and the manifest file.

2. **Development Mode**
   - Start the application with:
     ```bash
     python quargen.py dev --module MyApp
     ```
   - The DevServer changes the working directory to the parent level of `MyApp` and launches the app as a module
     (`python -m MyApp.main`), ensuring that relative imports are correctly resolved.
   - The `main.py` file automatically registers API, UI, Sockets, all controllers, and extra endpoints.

3. **Production Build**
   - Run the command:
     ```bash
     python quargen.py build --module MyApp
     ```
   - This command runs `npm install` and `npx webpack` to create a minimized version of the JS files, ready for production.

4. **Adding New Components**
   - Use the `add` command to add new classes or templates. For example:
     - **UI Template with Extra Endpoint:**
       ```bash
       python quargen.py add --type template --class_name CustomTemplate --module MyApp --url_prefix custom
       ```
     - **Extra API Endpoint:**
       ```bash
       python quargen.py add --type endpoint --class_name Extra_API --module MyApp --prefix extra
       ```
     - You can add controllers, services, and models by specifying the subtype (e.g., `rest`, `business`, `domain`, etc.).

5. **Colored Logger**
   - During execution, the `ColoredLogger` class produces colored logs in the console, making monitoring and debugging easier.

---

## What the Software Does

- **Automates the Generation of a Modular Structure:**  
  It creates a complete module for QuarTrend in a standardized way,
  including all necessary components for API, UI, sockets, and business logic.

- **Simplifies Startup and Build Management:**  
  Provides commands to start the app in development mode and to build the module for production using webpack.

- **Extensibility and Aggregation:**  
  All components implement standard interfaces, allowing automatic aggregation of logic from different modules into a cohesive project.

- **Colored Log Output:**  
  Thanks to the `ColoredLogger`, logs are displayed clearly and in color, aiding in debugging.

- **Centralized Template Management:**  
  UI and main templates are managed in specific folders (html_templates and py_templates) for easier maintenance.

- **Module Manifest:**  
  Each module generates a `module_manifest.json` file with module information, useful for future aggregation operations.

---

## Future Developments

- **Testing and CI/CD:**
  - Add more unit and integration tests.
  - Integrate a Continuous Integration system for automatic test execution.

- **Documentation and Log Improvements:**
  - Improve both internal and external documentation.
  - Update log messages for even more intuitive debugging.

- **Extensibility:**
  - Add new component types and customization options.
  - Support additional languages or frameworks in structure generation.

- **Build and Deploy Optimization:**
  - Integrate additional tools for minification and bundling.
  - Automate deployment to staging and production environments.

---

## Updates

This README is updated with every significant change to the project.  
*TODO: Keep this file updated with new features or changes.*

---

## How to Contribute

If you wish to contribute to QuarGen, fork the repository, make your changes, and open a pull request.
See the `CONTRIBUTING.md` file (if available) for contribution guidelines.

---

With QuarGen, you can quickly generate a standardized and scalable modular structure,
making development and integration of applications for the QuarTrend project much easier.
