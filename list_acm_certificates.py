'''List DNS validation records from ACM certificates'''
import boto3

def get_aws_profiles():
    '''Returns the AWS profiles and regions to use'''
    aws_profiles = {
        'disco_dev-admin' : 'eu-central-1',
        'disco_dev-admin' : 'us-east-1',
        'disco-admin' : 'eu-central-1',
        'disco-admin' : 'us-east-1',
        # 'unity_demo-admin': 'eu-central-1',
        # 'unity_dev-admin': 'eu-central-1',
        # 'unity_preprod-admin': 'eu-central-1',
        # 'unity_prod-admin': 'eu-central-1',
        # 'unity_staging-admin': 'eu-central-1',
        # 'unity_sandbox-admin': 'eu-central-1',
        }
    return aws_profiles

def get_paginated_aws(service: str,
                      method: str,
                      content: str,
                      options):
    values = []

    client = boto3.client(service)
    paginate = client.get_paginator(method)

    for page in paginate.paginate(options):
        for value in page[content]:
            values.append(value)

    return values

def get_certificates():
    '''Returns certificate'''
    certificates = []
    acm = boto3.client('acm')
    paginate_certificates = acm.get_paginator('list_certificates')

    for certificate_page in paginate_certificates.paginate():
        for certificate in certificate_page['CertificateSummaryList']:
            certificates.append(certificate)

    return certificates

def get_subject_alternative_names(certificate_arn : str):
    '''Returns the domain for which this certificate is valid (SAN or Subject Alternative Name)'''

    sans = []

    acm = boto3.client('acm')

    certificate=acm.describe_certificate(CertificateArn=certificate_arn)
    for san in certificate['Certificate']['SubjectAlternativeNames']:
        sans.append(san)

    return sans

def get_validation_records(certificate_arn : str):
    '''Returns certificate_arn's validation_records'''

    records = []
    acm = boto3.client('acm')

    certificate=acm.describe_certificate(CertificateArn=certificate_arn)
    for validation in certificate['Certificate']['DomainValidationOptions']:
        if validation['ValidationMethod'] == 'DNS':
            record=validation['ResourceRecord']
            records.append([record['Name'], record['Value']])

    return records

def main():
    '''Get ACM certificates'''

    print("Profile§Region§Certificate§Arn")
    for aws_profile, aws_region in get_aws_profiles().items():
        boto3.setup_default_session(region_name=aws_region, profile_name=aws_profile)
        certificates = get_certificates()
        # certificates = get_paginated_aws('acm', 'list_certificates', 'CertificateSummaryList')

        for certificate in certificates:
            print("§".join([aws_profile, aws_region, certificate['DomainName'], certificate['CertificateArn']]))

    print("Profile§Region§Arn§Domain")
    for aws_profile, aws_region in get_aws_profiles().items():
        boto3.setup_default_session(region_name=aws_region, profile_name=aws_profile)
        certificates = get_certificates()

        for certificate in certificates:
            if certificate['Status'] != 'EXPIRED':
                domains  = get_subject_alternative_names(certificate['CertificateArn'])
                for d in domains:
                    print(aws_profile, "§", aws_region, "§", certificate['CertificateArn'], "§", d)

    print("Profile§Region§Arn§Domain§ValidationName§ValidationValue")
    for aws_profile, aws_region in get_aws_profiles().items():
        boto3.setup_default_session(region_name=aws_region, profile_name=aws_profile)
        certificates = get_certificates()
        # certificates = get_paginated_aws('acm', 'list_certificates', 'CertificateSummaryList')

        for certificate in certificates:
            if certificate['Status'] != 'EXPIRED':
                validation_records = get_validation_records(certificate['CertificateArn'])
                for r in validation_records:
                    print(aws_profile, "§", aws_region, "§", certificate['CertificateArn'], "§", certificate['DomainName'], "§", "§".join(r))

if __name__ == "__main__":
    main()
