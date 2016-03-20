# -*- coding: utf-8 -*-
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json
import httplib2


def get_service(api_name, api_version, scope, key_file_location, service_account_email):
    credentials = ServiceAccountCredentials.from_p12_keyfile(
        service_account_email=service_account_email,
        filename=key_file_location,
        scopes=scope)
    http = credentials.authorize(httplib2.Http())

    # Build the service object.
    service = build(api_name, api_version, http=http)

    return service


def get_first_profile_id(service):
    # Use the Analytics service object to get the first profile id.

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(accountId=account).execute()

    if properties.get('items'):
        # Get the first property id.
        property = properties.get('items')[0].get('id')

        # Get a list of all views (profiles) for the first property.
        profiles = service.management().profiles().list(
            accountId=account,
            webPropertyId=property).execute()

        if profiles.get('items'):
            # return the first view (profile) id.
            return profiles.get('items')[0].get('id')

    return None


def get_rankings_results(service, profile_id, config):
    return service.data().ga().get(
        ids='ga:' + profile_id,
        start_date=config['start_date'],
        end_date=config['end_date'],
        sort='-ga:pageviews',
        max_results='10',
        dimensions='ga:pageTitle,ga:pagePath',
        metrics='ga:pageviews').execute()


def print_rankings_results(results, home):
    # Print data nicely for the user.
    if results:
        print(u'-----------ランキングTop10-----------')
        for col in results.get('rows'):
            print(u'{0}\t{1}{2}\t{3}'.format(col[0], home, col[1], col[2]))
    else:
        print ('No results found')


def main():
    # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/analytics.readonly']

    # 設定ファイルの読み込み
    config_file = open('config.json')
    config = json.load(config_file)
    config_file.close()
    service_account_email = config['email']
    key_file_location = config['key']

    # apiの呼び出し・結果出力
    service = get_service('analytics', 'v3', scope, key_file_location, service_account_email)
    profile = get_first_profile_id(service)
    print_rankings_results(get_rankings_results(service, profile, config), config['home'])

if __name__ == '__main__':
    main()