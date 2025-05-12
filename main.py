import argparse
import os
import re

from textwrap import shorten
from client import ask_ollama

# Interact with [./notes.txt] plain database
# Get prompt templates [./prompts/*] by mode
Prompts = {
    "summarize": "prompts/summarize.txt",
    "rewrite": "prompts/rewrite.txt",
    "question": "prompts/question.txt"
}

def ensure_file_exists(path, default_content=""):
    """Check and create file"""
    dir_name = os.path.dirname(path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
    if not os.path.exists(path):
        #print(f"[DEBUG] File not found, creating: {path}")
        with open(path, "w", encoding="utf-8") as f:
            f.write(default_content)

def load_notes(path="notes.txt"):
    """Load context from local notes.txt"""
    ensure_file_exists(path, "Take and edit notes here to establish context...\n")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
def touch_log(path="log.txt"):
    """Load context from local notes.txt"""
    ensure_file_exists(path, "Full conversation history and context logged here...\n")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
def load_prompt(template_path, **kwargs):
    """Load prompt template"""
    ensure_file_exists(template_path, "{text}")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
        for key, value in kwargs.items():
            template = template.replace(f"{{{key}}}", value)
        return template

def append_to_log(log_entry, path="log.txt"):
    """Append full entry to log.txt"""
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n\n--- LOG ENTRY ---\n")
        f.write(log_entry.strip())
        f.write("\n--- END ENTRY ---\n")

def append_to_notes(summary_line, path="notes.txt"):
    """Append a short summary to notes.txt"""
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n{summary_line.strip()}")

def main():
    # parse args 
    parser = argparse.ArgumentParser(description="Local AI Notes Assistant")
    parser.add_argument("--mode", choices=["summarize", "rewrite", "question"], default="summarize", help="Select mode of operation")
    parser.add_argument("--question", type=str, help="Question to ask (used only in 'question' mode)")
    args = parser.parse_args()

    # load context notes
    touch_log()
    notes = load_notes()
    
    # select prompt template
    if args.mode == "question":
        if not args.question:
            args.question = input("Enter your question: ")
        prompt = load_prompt(Prompts["question"], text=notes, question=args.question)
    else:
        prompt = load_prompt(Prompts[args.mode], text=notes)

    # ask model
    response = ask_ollama(prompt)

    # show reply
    print(f"\n--- mode: {args.mode} response: ---\n")
    print(response)

    # split and format output
    short_resp = ""
    long_resp = ""
    
    short_match = re.search(r"(?i)short answer[:\-]*\s*([\s\S]*?)\s*(?=full answer[:\-]*|$)", response)
    full_match = re.search(r"(?i)full answer[:\-]*\s*([\s\S]+)", response)

    if short_match:
        short_resp = short_match.group(1).strip()
    else:
        # fallback if a format unexpected
        short_resp = shorten(response.strip(), width=100, placeholder="...")
    
    short_resp = re.sub(r"[*_`#\-]+", "", short_resp).strip()

    if full_match:
        long_resp = full_match.group(1).strip()
    else:
        long_resp = response.strip()

    # add log
    log = f"[MODE] {args.mode}\n"
    if args.mode == "question":
        log += f"[QUESTION] {args.question}\n"
    log += f"[REPLY] {long_resp}{'...' if len(long_resp) > 5000 else ''}\n"
    append_to_log(log)

    # add context
    summary_line = f"{short_resp}"
    append_to_notes(summary_line)

if __name__ == "__main__":
    main()

# Usage example:
#
# python main.py --help
#
# python main.py --mode summarize
# python main.py --mode rewrite
# python main.py --mode question --question "How to cook mashed potato?"
