from abc import ABC
from typing import Iterable, Any

from app.models import ConsumeRequest, ProduceRequest

class BufferInterface(ABC):
    
    def consume(self) -> Iterable[tuple[Any, ConsumeRequest]]:
        """Consume requests from buffer (consumer channel), the buffer should be thread safe

        Returns:
            Iterable[tuple[Any, ConsumeRequest]]: Metadata (For acknowledgement) and Consumer request.
        """
        raise NotImplementedError("This is just a interface method!")
    
    def process(self, metadata: Any) -> None:
        """ Give acknowledgement to the buffer, confirming the request sucess process!

        Args:
            metadata (Any): Metadata used for process identification.
        """
        raise NotImplementedError("This is just a interface method!")
    
    def produce(self, produce_request: ProduceRequest) -> None:
        """ Produce a ProduceRequest on the buffer, to be used on other applications.

        Args:
            produce_request (ProduceRequest): Produce request to be used on other applications on the same buffer (producer channel).
        """
        raise NotImplementedError("This is just a interface method!")
    
    def add(self, consume_request: ConsumeRequest) -> None:
        """ Add a consume request on buffer (consume chanell), to testing propurses.

        Args:
            consume_request (ConsumeRequest): Consume request to be tested.
        """
        raise NotImplementedError("This is just a interface method!")
    