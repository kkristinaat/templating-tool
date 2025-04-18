import pytest
import subprocess
import os
from pathlib import Path


def test_docker_generator_blackbox():
    """
    Black box test for the Dockerfile generator.
    Tests that given the input file, the correct output is produced.
    """
    # Ensure the working directory has the necessary template directory
    cwd = Path.cwd()
    template_dir = cwd / "templates"
    template_dir.mkdir(exist_ok=True)
    
    # Copy the Dockerfile.j2 to templates directory if needed
    template_file = template_dir / "Dockerfile.j2"
    if not template_file.exists():
        original_template = cwd / "Dockerfile.j2"
        if original_template.exists():
            template_file.write_text(original_template.read_text())
    
    # Output path for the Dockerfile
    output_path = cwd / "test_output_Dockerfile"
    
    try:
        # Run the main.py script as a black box
        result = subprocess.run(
            ["python", "main.py"],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Check if the Dockerfile was created (the script creates "Dockerfile" by default)
        default_output = cwd / "Dockerfile"
        assert default_output.exists(), "Dockerfile was not created"
        
        # Verify the content matches the expected output
        dockerfile_content = default_output.read_text()
        
        # Expected output based on project.yaml content
        expected_content = """FROM ruby:3.0
LABEL maintainer="Your teammate"         # John Doe
WORKDIR /app
COPY . /app
RUN bundle install
CMD ["rails", "server"] # Startup command for MyAwesomeService."""
        
        assert dockerfile_content.strip() == expected_content.strip(), \
            f"Expected content doesn't match actual content.\nExpected:\n{expected_content}\n\nActual:\n{dockerfile_content}"
            
    finally:
        if default_output.exists():
            default_output.unlink()
        if output_path.exists():
            output_path.unlink()


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])