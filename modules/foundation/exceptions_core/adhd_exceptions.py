"""
This module defines the custom base exception for the ADHD Framework.
"""


class ADHDError(Exception):
    """
    Base exception for all anticipated, application-specific errors within the ADHD Framework.

    This exception should be used to wrap errors that arise from predictable failure
    modes, such as failed API calls, process execution errors, or complex validation
    failures. It allows the application to distinguish between known operational
    errors and unexpected bugs.

    Use `raise ADHDError("...") from original_exception` to preserve the original traceback.
    """
    pass
