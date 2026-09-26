#!/usr/bin/env python3
import argparse
import sys
from db.billing_db import fetch_invoices, fetch_account_totals, fetch_invoice_by_id

def main():
    parser = argparse.ArgumentParser(description="Billing Query Service")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inv_p = subparsers.add_parser("invoices", help="Query invoices for account")
    inv_p.add_argument("account_id", help="Account ID")
    inv_p.add_argument("--status", default=None, help="Filter by status")

    tot_p = subparsers.add_parser("totals", help="Get account totals")
    tot_p.add_argument("account_id", help="Account ID")

    inf_p = subparsers.add_parser("info", help="Get invoice details by ID")
    inf_p.add_argument("id", type=int, help="Invoice ID")

    args = parser.parse_args()

    if args.command == "invoices":
        invoices = fetch_invoices(args.account_id, status=args.status)
        for inv in invoices:
            print(f"[{inv['id']}] Account: {inv['account_id']} | Amount: ${inv['amount']:.2f} | Status: {inv['status']} | Due: {inv['due_date']}")
    elif args.command == "totals":
        totals = fetch_account_totals(args.account_id)
        print(f"Account: {args.account_id} | Invoices: {totals['count']} | Total: ${totals['total']:.2f}")
    elif args.command == "info":
        inv = fetch_invoice_by_id(args.id)
        if inv:
            print(f"[{inv['id']}] Account: {inv['account_id']} | Amount: ${inv['amount']:.2f} | Status: {inv['status']}")
        else:
            print("Invoice not found.")

if __name__ == "__main__":
    main()
