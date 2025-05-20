import pytest
from unittest.mock import patch
import main

@patch("main.run_pipeline")
def test_main_run(mock_run):
    main.main()
    mock_run.assert_called_once()
