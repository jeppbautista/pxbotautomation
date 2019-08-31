import pxbot
if __name__ == "__main__":
    pxbot = pxbot.Pxbot()
    wallet = 'payout'
    if pxbot.authenticate('jeppbautista23', 'Walangforever123'):
        metrics = pxbot.init_update()
        if metrics['expired'] != "Never":
            while metrics['earnings'] + metrics[wallet] >= 10.0:
                if 'successfully' in pxbot.transfer_finance(metrics['earnings'], wallet):
                    metrics['earnings'] -= 10
                    pxbot.buy_revshares(wallet)

        elif metrics['expired'] == "Never":
            while metrics['earnings'] >= 25:
                if 'successfully' in pxbot.transfer_finance(25, wallet):
                    metrics['earnings'] -= 25
                    pxbot.upgrade_membership(wallet)
