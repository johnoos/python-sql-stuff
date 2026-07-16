import io
import email_validator  # Replace with the actual name of your python file

def test_email_validation_output(monkeypatch, capsys):
    # 1. Define the simulated STDIN data from your second image
    simulated_input = (
        "6\n"
        "shashank <shashank@9mail.com>\n"
        "shashank <shashank@gmail.9om>\n"
        "shashank <shashank@gma_il.com>\n"
        "shashank <shashank@mail.moc>\n"
        "shashank <shashank@company-mail.com>\n"
        "shashank <shashank@companymail.c_o>\n"
    )

    # 2. Mock STDIN using monkeypatch and StringIO
    monkeypatch.setattr("sys.stdin", io.StringIO(simulated_input))

    # 3. Execute the main function from your script
    email_validator.main()
