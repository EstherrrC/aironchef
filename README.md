# Hackathon Project - *AIronChef*

Submitted by: **Five Golden Flowers**

**AIronChef** is an AI-powered meal assistant that leverages edge computing to help users plan meals and cook with voice guidance. By combining LLM technology with image recognition, AIronChef can suggest personalized recipes based on available ingredients and dietary restrictions, while providing hands-free cooking instructions.
 

## 🌟 Features
- [ ] 
- [ ] 
- [ ] 
- [ ] 
- [ ] 


## 👥 Team Members  
- **Brenda Jow** ([LinkedIn](https://www.linkedin.com/in/brendajow/)) - Developer  
- **Esther Chen** ([LinkedIn](https://www.linkedin.com/in/esther-chen-seattle)) - Developer 
- **Tzu-Chieh Yang** ([LinkedIn](https://www.linkedin.com/in/tzu-chieh-yang-221149290)) - Developer
- **Zhen Zhen** ([Email](mailto:zhenzhenzz0318@gmail.com)) - Developer
- **Zhiliang Yu** ([Email](mailto:zellayu1212@gmail.com)) - Developer


## 🚀 Setup Instructions (from scratch, including dependencies if applicable)

- [ ] 
- [ ] 
- [ ] 
- [ ] 
- [ ] 


## 🏃‍♂️ Running the Application
  
- [ ] 
- [ ] 
- [ ] 
- [ ] 
- [ ]


## 📱 Usage Instructions

- [ ] 
- [ ] 
- [ ] 
- [ ] 
- [ ]


## Nice to have, but not required, components include:

- [ ] Tests and testing instructions to verify the app setup
- [ ] Notes section containing additional information not covered in the app description
- [ ] References used while developing the app
- [ ] Well-commented code

## 🧪 Testing

## 📝 Notes

## 🔗 References

## Developer Setip Notes

# Setup Guide for Local Development

This README will guide you through setting up the project on your local computer. It includes the creation of a virtual environment, installation of dependencies, and troubleshooting steps.

## Prerequisites

Ensure that you have the following installed on your local machine:

- Python 3.x
- pip (Python's package manager)
- PowerShell (for Windows users)
- Terminal or Bash (for macOS/Linux users)

## Steps to Set Up the Project

### 1. Clone the Repository

Clone the repository to your local machine using the following command:

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a Virtual Environment

Navigate to the project directory and create a virtual environment to isolate your project dependencies:

#### For Windows (PowerShell):

```powershell
python3 -m venv llm-venv
```

#### For macOS/Linux (Terminal):

```bash
python3 -m venv llm-venv
```

This will create a new virtual environment called `llm-venv`.

### 3. Activate the Virtual Environment

#### For Windows (PowerShell):

```powershell
.\llm-venv\Scripts\Activate.ps1
```

#### For macOS/Linux (Terminal):

```bash
source llm-venv/bin/activate
```

You should now see `(llm-venv)` in your terminal, indicating that the virtual environment is active.

### 4. Install Dependencies

Install the necessary Python packages by using the `requirements.txt` file. This file contains all the packages required for the project:

```bash
pip install -r requirements.txt
```

*Note:* If you haven't already installed the `opencv-python` and `onnxruntime` libraries, you can manually install them by running:

```bash
pip install opencv-python onnxruntime
```

### 5. Check for Missing Files

You might encounter errors if certain files are missing. For example, the `config.yaml` file was not found initially. You can manually create the `config.yaml` file in the project directory with the following format:

```yaml
api_key: "EJ1VK5N-D084RGH-NKJDTGB-SV282YJ"
model_server_base_url: "http://localhost:3001/api/v1"
workspace_slug: "aihackathon"
```

If you already have this file in another location, you can copy it into the project directory:

#### For Windows (PowerShell):

```powershell
Copy-Item -Path C:\path\to\config.yaml -Destination .
```

#### For macOS/Linux (Terminal):

```bash
cp /path/to/config.yaml .
```

### 6. Running the Code

To run the chatbot script, use the following command:

```bash
python3 ./src/terminal_chatbot.py
```

This should start the chatbot, and you should be able to interact with it.

### 7. Troubleshooting

- **ModuleNotFoundError**: If you encounter an error like `ModuleNotFoundError: No module named 'requests'`, make sure that the virtual environment is activated and that all dependencies are installed by running:

  ```bash
  pip install -r requirements.txt
  ```

- **Missing `config.yaml`**: If the script asks for the `config.yaml` file, ensure it is manually created with the format provided in Step 5.

- **PowerShell Execution Policy (Windows Only)**: If you get an error when activating the virtual environment in PowerShell, you might need to adjust your execution policy. Run the following command in PowerShell as Administrator:

  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

This will allow you to run the script.

- **Checking Python Version and Path**: If you encounter issues with running Python scripts, confirm that you are using the correct Python version and virtual environment:

#### For Windows (PowerShell):

```powershell
python3 --version
where python3
```

#### For macOS/Linux (Terminal):

```bash
python3 --version
which python3
```

---

Now your environment should be set up and running! You can start interacting with the chatbot or work on other features of the project.



## 📄 License

- This project is licensed under the MIT License - see the LICENSE file for details.



