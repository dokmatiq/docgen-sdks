<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Builder;

use Dokmatiq\DocGen\Model\BankAccount;
use Dokmatiq\DocGen\Model\InvoiceData;
use Dokmatiq\DocGen\Model\InvoiceItem;
use Dokmatiq\DocGen\Model\InvoiceUnit;
use Dokmatiq\DocGen\Model\Party;
use Dokmatiq\DocGen\Model\XRechnungFormat;
use Dokmatiq\DocGen\Model\ZugferdProfile;

/**
 * Fluent builder for structured invoice data (ZUGFeRD/XRechnung).
 *
 * Usage:
 *   $invoice = $dg->invoice()
 *       ->number('RE-2026-001')
 *       ->date('2026-04-12')
 *       ->seller(new Party('ACME GmbH', 'Musterstr. 1', '10115', 'Berlin'))
 *       ->buyer(new Party('Kunde AG', 'Kundenweg 5', '20095', 'Hamburg'))
 *       ->item(new InvoiceItem('Beratung', 120.0, quantity: 8, unit: InvoiceUnit::HOUR))
 *       ->bank(new BankAccount('DE89370400440532013000'))
 *       ->build();
 */
final class InvoiceBuilder
{
    private ?string $number = null;
    private ?string $date = null;
    private ?Party $seller = null;
    private ?Party $buyer = null;
    /** @var InvoiceItem[] */
    private array $items = [];
    private string $currency = 'EUR';
    private ?BankAccount $bankAccount = null;
    private ?string $paymentTerms = null;
    private ?string $dueDate = null;
    private ?string $note = null;
    private ?string $buyerReference = null;
    private string $typeCode = '380';
    private ZugferdProfile $profile = ZugferdProfile::EN16931;
    private ?XRechnungFormat $xrechnungFormat = null;

    public function number(string $number): self { $this->number = $number; return $this; }
    public function date(string $date): self { $this->date = $date; return $this; }
    public function seller(Party $seller): self { $this->seller = $seller; return $this; }
    public function buyer(Party $buyer): self { $this->buyer = $buyer; return $this; }
    public function item(InvoiceItem $item): self { $this->items[] = $item; return $this; }

    public function addItem(string $description, float $unitPrice, float $quantity = 1, ?InvoiceUnit $unit = null, float $vatRate = 19.0): self
    {
        $this->items[] = new InvoiceItem($description, $unitPrice, $quantity, $unit, $vatRate);
        return $this;
    }

    public function currency(string $code): self { $this->currency = $code; return $this; }
    public function bank(BankAccount $account): self { $this->bankAccount = $account; return $this; }
    public function paymentTerms(string $terms): self { $this->paymentTerms = $terms; return $this; }
    public function dueDate(string $dueDate): self { $this->dueDate = $dueDate; return $this; }
    public function note(string $note): self { $this->note = $note; return $this; }
    public function buyerReference(string $ref): self { $this->buyerReference = $ref; return $this; }
    public function typeCode(string $code): self { $this->typeCode = $code; return $this; }
    public function profile(ZugferdProfile $profile): self { $this->profile = $profile; return $this; }
    public function xrechnung(?XRechnungFormat $format = XRechnungFormat::CII): self { $this->xrechnungFormat = $format; return $this; }

    public function build(): InvoiceData
    {
        if ($this->number === null) throw new \InvalidArgumentException('Invoice number is required');
        if ($this->date === null) throw new \InvalidArgumentException('Invoice date is required');
        if ($this->seller === null) throw new \InvalidArgumentException('Seller is required');
        if ($this->buyer === null) throw new \InvalidArgumentException('Buyer is required');

        return new InvoiceData(
            number: $this->number,
            date: $this->date,
            seller: $this->seller,
            buyer: $this->buyer,
            items: $this->items,
            currency: $this->currency,
            bankAccount: $this->bankAccount,
            paymentTerms: $this->paymentTerms,
            dueDate: $this->dueDate,
            note: $this->note,
            buyerReference: $this->buyerReference,
            typeCode: $this->typeCode,
            profile: $this->profile,
            xrechnungFormat: $this->xrechnungFormat,
        );
    }
}
