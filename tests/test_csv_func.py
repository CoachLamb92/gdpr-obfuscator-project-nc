from src.csv_func import obfuscate


def test_returns_string():
    # Arrange
    with open("testing_files/test_data.csv", "r") as f:
        data = f.read()
    columns = ["email_address"]
    # Act
    result = obfuscate(data, columns)
    # Assert
    if not isinstance(result, str):
        raise AssertionError(
            f"\n{result}\nis not of type string"
            )


def test_returns_unchanged_data():
    # Arrange
    columns = []
    with open("testing_files/test_data.csv", "r") as f:
        original = f.read()
    data = original
    # Act
    result = obfuscate(data, columns)
    # Assert
    if original != result:
        raise AssertionError(
            "Original data is different to resultant data"
            )


def test_returns_changed_data():
    # Arrange
    columns = ["name"]
    with open("testing_files/test_data.csv", "r") as f:
        original = f.read()
    data = original
    # Act
    result = obfuscate(data, columns)
    # Assert
    if original == result:
        raise AssertionError(
            "Original data is the same as resultant data"
            )


def test_returns_obfuscated_name_data():
    # Arrange
    with open("testing_files/test_data.csv", "r") as f:
        data = f.read()
    columns = ["name"]
    expected = [
        "student_id,name,course,cohort,graduation_date,email_address",
        "1,'***','Software','December','2024-03-31','j.smith@email.com'",
        "2,'***','Software','March','1999-08-01','j.doe@email.com'",
        "3,'***','Hardware','September','2022-12-21','m.jones@email.com'",
        "4,'***','Mechanics','March','2005-01-29','annepwhite@email.com'"
        ]
    # Act
    result = obfuscate(data, columns)
    # Assert
    if "\n".join(expected) != result:
        raise AssertionError(
            "Result has not returned correctly"
            )


def test_returns_obfuscated_email_data():
    # Arrange
    with open("testing_files/test_data.csv", "r") as f:
        data = f.read()
    columns = ["email_address"]
    expected = [
        "student_id,name,course,cohort,graduation_date,email_address",
        "1,'John Smith','Software','December','2024-03-31','***'",
        "2,'Jane Doe','Software','March','1999-08-01','***'",
        "3,'Mike Jones','Hardware','September','2022-12-21','***'",
        "4,'Anne White','Mechanics','March','2005-01-29','***'"
        ]
    # Act
    result = obfuscate(data, columns)
    # Assert
    if "\n".join(expected) != result:
        raise AssertionError(
            "Result has not returned correctly"
        )


def test_returns_obfuscated_name_and_email_data():
    # Arrange
    with open("testing_files/test_data.csv", "r") as f:
        data = f.read()
    columns = ["name", "email_address"]
    expected = [
        "student_id,name,course,cohort,graduation_date,email_address",
        "1,'***','Software','December','2024-03-31','***'",
        "2,'***','Software','March','1999-08-01','***'",
        "3,'***','Hardware','September','2022-12-21','***'",
        "4,'***','Mechanics','March','2005-01-29','***'"
        ]
    # Act
    result = obfuscate(data, columns)
    # Assert
    if "\n".join(expected) != result:
        raise AssertionError(
            "Result has not returned correctly"
        )
