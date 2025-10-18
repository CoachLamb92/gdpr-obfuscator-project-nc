def obfuscate(data: str, columns: list[str]) -> str:
    """Obfuscates specific columns in a CSV

    Returns a string representing a CSV file where selected data are
    replaced by '***' to uphold GDPR

    Args:
        data (str): the untouched data
        columns (list[str]): a list of column headers to be obfuscated

    Returns:
        obfuscated_data (str): the newly obfuscated data
    """

    output = []
    rows = data.split("\n")
    output.append(rows[0])
    indexes_to_obfuscate = [
        rows[0].split(",").index(column) for column in columns
        ]
    for row in rows[1:]:
        row = row.split(",")
        for index in indexes_to_obfuscate:
            row[index] = "'***'"
        output.append(",".join(row))
    obfuscated_data = "\n".join(output)
    return obfuscated_data
