import io
import py_CSScolour_validator

def test_email_validation_output(monkeypatch, capsys):
    # 1. Define the simulated STDIN data from your second image
    simulated_input = (
        "24\n"
        ".custom-file-input::-webkit-file-upload-button {\n"
        "   visibility: hidden;\n"
        "}\n"
        ".custom-file-input::before {\n"
        "   content: 'Select some files';\n"
        "   display: inline-block;\n"
        "   background: -webkit-linear-gradient(top, #f9f9f9, #e3e3e3);\n"
        "   border: 1px solid #999;\n"
        "   border-radius: 3px;\n"
        "   padding: 5px 8px;\n"
        "   outline: none;\n"
        "   white-space: nowrap;\n"
        "   -webkit-user-select: none;\n"
        "   cursor: pointer;\n"
        "   text-shadow: 1px 1px #fff;\n"
        "   font-weight: 700;\n"
        "   font-size: 10pt;\n"
        "}\n"
        ".custom-file-input:hover::before {\n"
        "border-color: black;\n"
        "}\n"
        ".custom-file-input:active::before {\n"
        "   background: -webkit-linear-gradient(top, #e3e3e3, #f9f9f9);\n"
        "}\n"
    )

    # 2. Mock STDIN using monkeypatch and StringIO
    monkeypatch.setattr("sys.stdin", io.StringIO(simulated_input))

    # 3. Execute the main function from your script
    py_CSScolour_validator.main()