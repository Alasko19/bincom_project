from django.shortcuts import render, redirect
from django.db.models import Sum
from django.utils import timezone
from .models import PollingUnit, AnnouncedPuResults, Lga, Party

def level_1_pu_results(request):
    """
    Level 1: Display result for any individual Polling Unit.
    """
    polling_units = PollingUnit.objects.exclude(polling_unit_name__isnull=True).exclude(polling_unit_name__exact='')
    selected_pu_id = request.GET.get('pu_id')
    
    results = None
    selected_pu = None
    
    if selected_pu_id:
        try:
            selected_pu = PollingUnit.objects.get(uniqueid=selected_pu_id)
            results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=str(selected_pu_id))
        except PollingUnit.DoesNotExist:
            results = []

    context = {
        'polling_units': polling_units,
        'selected_pu': selected_pu,
        'results': results,
        'selected_pu_id': selected_pu_id
    }
    return render(request, 'polling_unit/question1_pu_result.html', context)


def level_2_lga_results(request):
    """
    Level 2: Sum total result of all polling units under a selected Local Government Area (LGA).
    """
    lgas = Lga.objects.all().order_by('lga_name')
    selected_lga_id = request.GET.get('lga_id')
    
    party_totals = []
    selected_lga = None
    total_lga_votes = 0

    if selected_lga_id:
        try:
            selected_lga = Lga.objects.get(lga_id=selected_lga_id)
            
            # Find all Polling Unit unique IDs in this LGA
            pu_uniqueids = PollingUnit.objects.filter(lga_id=selected_lga_id).values_list('uniqueid', flat=True)
            pu_str_ids = [str(uid) for uid in pu_uniqueids]

            # Aggregate scores grouped by Party
            party_scores = (
                AnnouncedPuResults.objects.filter(polling_unit_uniqueid__in=pu_str_ids)
                .values('party_abbreviation')
                .annotate(total_score=Sum('party_score'))
                .order_by('-total_score')
            )
            
            party_totals = party_scores
            total_lga_votes = sum(item['total_score'] for item in party_scores if item['total_score'])

        except Lga.DoesNotExist:
            pass

    context = {
        'lgas': lgas,
        'selected_lga': selected_lga,
        'party_totals': party_totals,
        'total_lga_votes': total_lga_votes,
        'selected_lga_id': selected_lga_id
    }
    return render(request, 'polling/question2_lga_result.html', context)


def level_3_add_pu(request):
    """
    Level 3: Page to add results for a new Polling Unit for all registered parties.
    """
    lgas = Lga.objects.all().order_by('lga_name')
    parties = Party.objects.all()

    if request.method == 'POST':
        pu_name = request.POST.get('pu_name')
        pu_number = request.POST.get('pu_number')
        lga_id = request.POST.get('lga_id')
        ward_id = request.POST.get('ward_id', 1)
        
        user_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        now = timezone.now()

        # Create new Polling Unit
        new_pu = PollingUnit.objects.create(
            polling_unit_name=pu_name,
            polling_unit_number=pu_number,
            lga_id=lga_id,
            ward_id=ward_id,
            entered_by_user="Admin User",
            date_entered=now,
            user_ip_address=user_ip
        )

        # Save score for each party submitted in the form
        for party in parties:
            score = request.POST.get(f'party_{party.partyid}', 0)
            AnnouncedPuResults.objects.create(
                polling_unit_uniqueid=str(new_pu.uniqueid),
                party_abbreviation=party.partyid,
                party_score=int(score) if score else 0,
                entered_by_user="Admin User",
                date_entered=now,
                user_ip_address=user_ip
            )

        return redirect(f'/?pu_id={new_pu.uniqueid}')

    context = {
        'lgas': lgas,
        'parties': parties
    }
    return render(request, 'polling/question3_add_pu.html', context)
