using System.Text.Json.Serialization;

namespace Dokmatiq.DocGen.Models;

[JsonConverter(typeof(JsonStringEnumConverter))]
public enum OutputFormat { PDF, DOCX, ODT }

[JsonConverter(typeof(JsonStringEnumConverter))]
public enum JobStatus { PENDING, PROCESSING, COMPLETED, FAILED }

[JsonConverter(typeof(JsonStringEnumConverter))]
public enum ZugferdProfile { MINIMUM, BASIC_WL, BASIC, EN16931, EXTENDED, XRECHNUNG }

[JsonConverter(typeof(JsonStringEnumConverter))]
public enum XRechnungFormat { CII, UBL }

[JsonConverter(typeof(JsonStringEnumConverter))]
public enum BarcodeFormat { CODE_128, CODE_39, EAN_13, EAN_8, UPC_A, QR_CODE, DATA_MATRIX, PDF_417 }

[JsonConverter(typeof(JsonStringEnumConverter))]
public enum InvoiceUnit { PIECE, HOUR, DAY, KILOGRAM, METER, LITER, SQUARE_METER }

[JsonConverter(typeof(JsonStringEnumConverter))]
public enum PaperSize { A4, A3, A5, LETTER, LEGAL }

[JsonConverter(typeof(JsonStringEnumConverter))]
public enum PageOrientation { PORTRAIT, LANDSCAPE }

[JsonConverter(typeof(JsonStringEnumConverter))]
public enum TextAlignment { LEFT, CENTER, RIGHT, JUSTIFY }
