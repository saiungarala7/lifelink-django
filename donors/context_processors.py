from donors.models import DonationReward


def donor_rewards_status(request):
    """
    Adds reward availability flag for donor navbar
    """
    if request.user.is_authenticated and hasattr(request.user, 'donor_profile'):
        has_rewards = DonationReward.objects.filter(
            donor=request.user.donor_profile
        ).exists()
        return {'donor_has_rewards': has_rewards}

    return {}
