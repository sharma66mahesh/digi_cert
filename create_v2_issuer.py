#!/usr/bin/env python
'''
Generates the issuer file (.json) thar represents the issues which is needed for issuing and validating certificates.

Currently, just not check for inputs' validity (e.g. valid address, URLs, etc.)
'''
import os
import sys
from cert_schema import *
import configargparse
import json

from cert_tools import helpers

ISSUER_TYPE = 'Profile'

OPEN_BADGES_V2_CONTEXT_JSON = OPEN_BADGES_V2_CANONICAL_CONTEXT
BLOCKCERTS_V2_CONTEXT_JSON = BLOCKCERTS_V2_CANONICAL_CONTEXT


def generate_issuer_file(config):

    if config.public_key_created:
        issued_on = config.public_key_created
    else:
        issued_on = helpers.create_iso8601_tz()
    output_handle = open(config.output_file, 'w') if config.output_file else sys.stdout

    context = [OPEN_BADGES_V2_CONTEXT_JSON, BLOCKCERTS_V2_CONTEXT_JSON]

    issuer_json = {
        '@context': context,
        'id': config.issuer_id,
        'url': config.issuer_url,
        'name': config.issuer_name,
        'email': config.issuer_email,
        'image': helpers.encode_image(os.path.join(config.abs_data_dir, config.issuer_logo_file)),
        'publicKey': [{'id': config.issuer_public_key, "created": issued_on}],
        'revocationList': config.revocation_list_uri,
        'type': ISSUER_TYPE
    }

    if config.intro_url:
        issuer_json['introductionUrl'] = config.intro_url

    output_handle.write(json.dumps(issuer_json, indent=2))

    if output_handle is not sys.stdout:
        output_handle.close()


def get_config():
    cwd = os.getcwd()
    print(os.path.join(cwd, 'conf.ini'))
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(cwd, 'cert_tools/conf.ini')])
    p.add('-c', '--my-config', required=True, is_config_file=True, help='config file path')
    p.add_argument('--data_dir', type=str, help='where data files are located')
    p.add_argument('-k', '--issuer_public_key', type=str, required=True, help='The key(s) an issuer uses to sign Assertions. See https://openbadgespec.org/#Profile for more details')
    p.add_argument('-k', '--public_key_created', type=str, help='ISO8601-formatted date the issuer public key should be considered active')
    p.add_argument('-r', '--revocation_list_uri', type=str, required=True, help='URI of the Revocation List used for marking revocation. See https://openbadgespec.org/#Profile for more details')
    p.add_argument('-d', '--issuer_id', type=str, required=True, help='the issuer\'s publicly accessible identification file; i.e. URL of the file generated by this tool')
    p.add_argument('-u', '--issuer_url', type=str, help='the issuer\'s main URL address')
    p.add_argument('-n', '--issuer_name', type=str, help='the issuer\'s name')
    p.add_argument('-e', '--issuer_email', type=str, help='the issuer\'s email')
    p.add_argument('-m', '--issuer_logo_file', type=str, help='the issuer\' logo image')
    p.add_argument('-i', '--intro_url', required=False, type=str, help='the issuer\'s introduction URL address')
    p.add_argument('-o', '--output_file', type=str, help='the output file to save the issuer\'s identification file')
    args, _ = p.parse_known_args()
    args.abs_data_dir = os.path.abspath(os.path.join(cwd, args.data_dir))
    print(args.abs_data_dir) 
    print(os.path.join(args.abs_data_dir, args.issuer_logo_file))   

    return args


def main():
    conf = get_config()
    generate_issuer_file(conf)


if __name__ == "__main__":
    main()

