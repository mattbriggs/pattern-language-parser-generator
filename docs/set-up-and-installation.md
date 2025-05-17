# ⚙️ Set up and installation of the Pattern Language Miner

This guide outlines the installation and usage of the Pattern Language Miner. It involves cloning the repository, creating a virtual environment, installing dependencies, and setting up Weaviate for semantic clustering. The tool can be run using the CLI to analyze a directory of files and generate patterns.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/pattern-language-miner.git
cd pattern-language-miner
```

### 2. Create a virtual environment

Create the virtual environment for your OS. Make sure your VS Code workspace uses `.venv` as the Python interpreter.

**Windows**:

```Powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**MacOS**:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```
## 📦 NLTK Setup

I've included a script to help get the resources you need. Also note that the NLTK is a previous version (3.7).

You can run:

```bash
python setup_resources.py
```

## 🧠 Weaviate (Vector Search)

The tool integrates with a local Weaviate instance for semantic clustering. 

[Weaviate](https://weaviate.io/) is an open-source, AI-native vector database designed to store and search data objects alongside their vector embeddings. This enables efficient similarity searches across various data types, including text, images, and other unstructured content. By leveraging machine learning models, Weaviate transforms data into high-dimensional vectors, facilitating semantic understanding and retrieval based on meaning rather than exact matches

### 1. Export your OpenAI API key (for text2vec)

Set OPENAI_APIKEY environment variable for Windows and macOS.

**Windows**:
```powershell
$env:OPENAI_APIKEY = "your-openai-key"
```

**MacOS**:

```bash
export OPENAI_APIKEY=your-openai-key
```

OpenAI provides powerful APIs that enable developers to integrate advanced AI models such as GPT-4 and ChatGPT into their applications. These APIs empower you to build intelligent features like natural language understanding, text generation, summarization, and question-answering capabilities. To access these models, you'll need an OpenAI API key, available after registering at [pplatform.openai.com](https://pplatform.openai.com).

Your API key securely authenticates your requests, tracks usage, and ensures data privacy. To use it, include the key in your HTTP headers when making API requests. OpenAI APIs offer flexibility with easy integration through RESTful endpoints, alongside comprehensive documentation and SDKs in Python, Node.js, and other languages. Usage is billed based on token consumption, giving you control over costs. OpenAI's API infrastructure supports applications from prototyping and experimentation to production deployment at scale, simplifying the addition of sophisticated AI-driven functionality into your software.

### 2. Start Weaviate using Docker

Load Docker compose file and check availability. The Docker Compose file defines a single containerized service named weaviate configured to run the Weaviate vector database with OpenAI integration.

1. Install Docker Desktop if not already installed. 
2. Load the Docker [compose file](docker-compose.yml).
    ```bash
    docker compose -f docker-compose.yml up -d
    ```
3.  Check availability: [http://localhost:8080/v1/.well-known/ready](http://localhost:8080/v1/.well-known/ready)

[Docker](https://www.docker.com/) is an open-source platform designed to simplify software development and deployment by packaging applications into standardized, portable containers. These containers bundle applications along with their dependencies, ensuring consistent behavior across various environments. Docker streamlines workflows, reduces conflicts between dependencies, and enhances resource utilization, making application delivery faster and more reliable.

Docker Desktop extends this capability by providing an intuitive graphical interface and additional tools tailored for local development on Windows, macOS, and Linux. It simplifies managing container lifecycles, networking, volume management, and orchestrating complex applications. Docker Desktop also includes built-in integrations with Kubernetes, enabling users to deploy and test containerized applications seamlessly on their local machines.

## 🚀 Running the tool

Use the CLI to analyze a directory of files:

```bash
PYTHONPATH=src python3 -m pattern_language_miner.cli \
--log-level DEBUG \
analyze \
  --input-dir ./sample_docs analyze\
  --output-dir ./patterns_output \
```

For further details about using the tool, see [Patter Miner CookBook](workflow.md).

## 🧪 Running Tests

```bash
PYTHONPATH=src pytest
```
## 🛠 Maintenance

* Use `requirements.txt` for consistent dependency versions.
* Clear `weaviate_data/` volume if you need to reset Weaviate.
* New document types can be added by implementing a new `BaseParser`.

For further details about resolving issues, see [Logging and Troubleshooting Guide](docs/troubleshooting.md).

## 📁 Project Structure

The Pattern Language Miner tool is designed for pattern extraction and generation. It includes a parser, extractor, output, vector store, and utilities, with documentation and tests.

```
docs/                    # Insructions and notes on how to use this tool
logs/                    # Location of the log files when debugging
src/pattern_language_miner/
├── parser/              # File parsers for text, HTML, markdown
├── extractor/           # Lexical and semantic pattern extractors
├── output/              # YAML and assembly writer
├── vector_store/        # Weaviate vector store client
├── utils/               # Logging and progress tools
├── cli.py               # CLI entry point
├── schema/              # JSON schema for pattern validation
tests/                   # Unit + integration tests
docker-compose.yml       # Weaviate container config
requirements.txt         # Script dependencies
setup_resources.py       # Script to install NLTK resources
```

For further details about the design of the tool, see [Pattern Language Miner: A Corpus-Driven Pattern Extraction and Generation Tool](docs/application-design.md).

# Related content

* [Command Reference](docs/command-reference.md)
* [config.yml Reference and Usage Guide](docs/configuration-file-reference.md)
* [Instructions for Docker and Weaviate Integration](docs/instructions_for_docker.md)
* [Pattern Language Miner: A Corpus-Driven Pattern Extraction and Generation Tool](docs/application-design.md)
* [Pattern Language Miner: How-To Manual](docs/application-guide.md)
* [Troubleshooting](docs/troubleshooting.md)
* [Workflow](docs/workflow.md)