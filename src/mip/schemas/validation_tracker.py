'''
validation_tracker.py

Shared validation helper used accross seed_data.py and csv_loader.py . Tracks per-record validation failure 
and enforces an abort threshold so a systemic schema/data bug doesn't silently pass as just some bad rows.

'''

import logging
from pydantic import BaseModel , ValidationError as PydanticValidationError


from mip import exceptions

logger = logging.getLogger(__name__)


class ValidationTracker:

    '''
    Tracks validation attempts across a batch of records.

    - processed: total records attempted (pass + fail)
    - failed: total records that failed validation
    - failures: bounded list of {raw_record, reason} for failed records
    
    '''
    # below name class constant is used to check the rate of failure , setting to 10 so that to get rate failure , but change it depending on the total number of records 
    MIN_SAMPLE_SIZE_FOR_RATE_CHECK = 10

    def __init__(self , max_failures: int | None = None , max_failure_rate: float | None = None) :

        self.processed = 0 
        self.failed = 0 
        self.failures: list[dict] = []
        self.max_failures = max_failures
        self.max_failure_rate = max_failure_rate

    def record_success(self) -> None:
        self.processed +=  1 

    def record_failure(self , raw_record: dict , reason: str) -> None :

        self.processed += 1 
        self.failed += 1 
        self.failures.append({"record" : raw_record , "reason" : reason})
        logger.warning(f"Validation failed: {reason} | record={raw_record}")
        self._check_abort()

    def _check_abort(self) -> None :


        if self.max_failures is not None and self.failed >= self.max_failures:
            raise exceptions.ValidationError(
                f"Aborting: failure count {self.failed} exceeded max_falure= {self.max_failures}"
            )

        if self.max_failure_rate is not None and self.processed >= self.MIN_SAMPLE_SIZE_FOR_RATE_CHECK:

            rate = self.failed / self.processed
            if rate > self. max_failure_rate:
                raise exceptions.ValidationError(
                    f"Aborting: failure rate {rate:.1%} exceeded max_failure_rate = {self.max_failure_rate:.0%}"
                    f"({self.failed}/{self.processed} records failed)"
                )           



def validate_record(

        schema_cls : type[BaseModel] , 
        raw_record : dict  , 
        tracker : ValidationTracker , 
) -> BaseModel | None :
    """
    Validate one raw dict against a Pydantic schema.

    On success : reports to tracker , returns the validated model instance
    On failure : reports to tracker ( which logs + may abort) , return None.

    Callers should skip the record when this returns None.

    """
    try:

        validated = schema_cls.model_validate(raw_record)
    except PydanticValidationError as e :

        first_error = e.errors()[0]
        field = first_error['loc'][0] if first_error['loc'] else "unknown"
        reason = f"field '{field}' {first_error['msg']}"
        tracker.record_failure(raw_record , reason)
        return None

    tracker.record_success()
    return validated 
            