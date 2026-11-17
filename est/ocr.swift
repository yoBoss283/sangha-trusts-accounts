// Read a scanned PDF with the Mac's built-in text recognition (Vision) and print every piece of text found,
// one per line: page <tab> x <tab> y <tab> width <tab> height <tab> text   (x, y from the top-left, as fractions of the page).
// extract.py lays these out again into columns. Build: swiftc -O ocr.swift -o ocr   Run: ./ocr file.pdf
import Foundation
import PDFKit
import Vision

guard CommandLine.arguments.count == 2, let doc = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[1])) else {
    FileHandle.standardError.write("usage: ocr file.pdf\n".data(using: .utf8)!); exit(1)
}
for i in 0..<doc.pageCount {
    guard let page = doc.page(at: i) else { continue }
    let box = page.bounds(for: .mediaBox)
    let scale = 2600.0 / max(box.width, box.height)            // about 300 dpi for an A4 page
    let img = page.thumbnail(of: CGSize(width: box.width * scale, height: box.height * scale), for: .mediaBox)
    guard let tiff = img.tiffRepresentation, let rep = NSBitmapImageRep(data: tiff), let cg = rep.cgImage else { continue }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false                         // keep figures exactly as printed
    req.recognitionLanguages = ["en-GB"]
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    for o in (req.results ?? []) {
        guard let t = o.topCandidates(1).first?.string else { continue }
        let b = o.boundingBox
        print(String(format: "%d\t%.4f\t%.4f\t%.4f\t%.4f\t", i + 1, b.minX, 1 - b.maxY, b.width, b.height) + t)
    }
}
