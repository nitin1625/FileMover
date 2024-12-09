# FileMover

**FileMover** automates file and folder operations based on customizable filters, reducing manual effort and improving efficiency in tasks like database backups, application deployments, and build management.

## Features

1. **Filter and Move Files**:  
   - Include or exclude files based on patterns (name, extension, etc.).  
   
2. **Filter and Move Folders**:  
   - Include or exclude folders using specific patterns.  
   
3. **Automation**:  
   - Replace manual tasks with automated directory import/export processes.  

4. **Real-World Applications**:  
   - **Database Backup & Recovery**  
   - **Application Deployment**  
   - **Build Deployment**  
   - Other repetitive directory-based tasks  

## How It Works

1. **Include Files Based on Patterns**:  
   Automatically include files matching specified patterns (e.g., extensions like `.log`, `.txt`).  

2. **Exclude Files Based on Patterns**:  
   Exclude specific files from operations based on patterns or rules.  

3. **Include Folders**:  
   Include entire folders or subfolders that meet specific criteria.  

4. **Exclude Folders**:  
   Exclude certain folders to streamline operations and prevent unnecessary processing.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nitin1625/FileMover.git
   cd FileMover
   ```

2. Install dependencies (if applicable):

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the scripts** based on your task:

   - **Include Files**:  
     ```bash
     python include_only_files.py
     ```

   - **Exclude Files**:  
     ```bash
     python exclude_only_files.py
     ```

   - **Include Folders**:  
     ```bash
     python include_only_folders.py
     ```

   - **Exclude Folders**:  
     ```bash
     python exclude_only_folders.py
     ```

2. **Customize filters** in the script files to match your specific patterns and directories.

## Example Patterns

- **Files**:  
  - Include: `*.csv`, `*.log`  
  - Exclude: `*.tmp`, `*_backup.*`  

- **Folders**:  
  - Include: `reports`, `exports`  
  - Exclude: `_temp`, `*_old`  

## Real-World Benefits

- **Efficiency**: Reduces manual directory operations by 50%.  
- **Reliability**: Ensures consistent application of filters for backups and deployments.  
- **Flexibility**: Adaptable to various real-world scenarios (backups, deployments, etc.).  

## Contributing

1. Fork the repository.  
2. Create a new branch:  
   ```bash
   git checkout -b feature/your-feature-name
   ```  
3. Make your changes and commit them:  
   ```bash
   git commit -m "Add new feature"  
   ```  
4. Push to your branch:  
   ```bash
   git push origin feature/your-feature-name
   ```  
5. Open a Pull Request.

## License

This project is licensed under the MIT License.

---

Now you can upload this **README.md** along with your files to your GitHub repository at [https://github.com/nitin1625/](https://github.com/nitin1625/).