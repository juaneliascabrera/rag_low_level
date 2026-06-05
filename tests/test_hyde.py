import pytest
from unittest.mock import Mock
from retrieval.hyde import HyDETransformer


class TestHyDETransformer:
    def test_transform(self):
        mock_llm = Mock()
        mock_llm.generate.return_value = "GDT is a table that contains segment descriptors..."
        
        hyde = HyDETransformer(mock_llm)
        result = hyde.transform("What is GDT?")
        
        assert isinstance(result, str)
        assert len(result) > 0
        mock_llm.generate.assert_called_once()

    def test_transform_calls_llm_with_correct_prompt(self):
        mock_llm = Mock()
        mock_llm.generate.return_value = "Technical document"
        
        hyde = HyDETransformer(mock_llm)
        hyde.transform("Explain IDT")
        
        call_args = mock_llm.generate.call_args
        assert "IDT" in call_args[0][1] or "IDT" in str(call_args)
