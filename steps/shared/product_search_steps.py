# steps/shared/product_search_steps.py

from pytest_bdd import given, when, then, parsers
import time
import statistics
from targets.web.pages.search_page import WebSearchPage
from targets.mobile.screens.search_screen import MobileSearchScreen
from targets.api.services.product_service import ProductService

@given(parsers.parse('the system has the following "{entity_type}":'))
def setup_system_data(context, entity_type, table):
    """Set up the system with the specified data."""
    # Convert table to list of dictionaries
    entities = []
    for row in table:
        entity = dict(row)
        # Convert numeric values
        for key in ['id', 'price', 'stock']:
            if key in entity:
                try:
                    if '.' in entity[key]:
                        entity[key] = float(entity[key])
                    else:
                        entity[key] = int(entity[key])
                except ValueError:
                    pass  # Keep as string if conversion fails
        entities.append(entity)
    
    # Store in context for use in other steps
    context[entity_type] = entities
    
    # Depending on test platform, set up data differently
    platform = context.get('platform', 'api')  # Default to API if not specified
    
    if platform == 'api':
        product_service = ProductService(context.get('api_client'))
        product_service.setup_test_data(entity_type, entities)
    else:
        pass