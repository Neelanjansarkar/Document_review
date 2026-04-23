from app.utils.file_utils import safe_filename


def test_safe_filename_removes_path_separators() -> None:
    assert safe_filename("../demo file.pdf") == "_demo_file.pdf"
