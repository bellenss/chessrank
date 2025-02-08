from django.shortcuts import render
from .utils import FIDEClient

def view_registered_tournaments(request):
    """Fetch and display the registered tournaments from FIDE"""
    try:
        html_content = FIDEClient.fetch_registered_tournaments()
    except Exception as e:
        html_content = str(e)  # Display error message

    return render(request, 'fide_registrations/registered_tournaments.html', {'html_content': html_content})
