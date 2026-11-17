// Save one page of a PDF as a PNG, for reading figures by eye. Build: swiftc -O page.swift -o page
// Run: ./page file.pdf <page number from 1> out.png
import Foundation
import PDFKit

let a = CommandLine.arguments
guard a.count == 4, let doc = PDFDocument(url: URL(fileURLWithPath: a[1])), let n = Int(a[2]),
      let page = doc.page(at: n - 1) else {
    FileHandle.standardError.write("usage: page file.pdf <page> out.png\n".data(using: .utf8)!); exit(1)
}
let box = page.bounds(for: .mediaBox)
let scale = 1800.0 / max(box.width, box.height)
let img = page.thumbnail(of: CGSize(width: box.width * scale, height: box.height * scale), for: .mediaBox)
guard let tiff = img.tiffRepresentation, let rep = NSBitmapImageRep(data: tiff),
      let png = rep.representation(using: .png, properties: [:]) else { exit(1) }
try! png.write(to: URL(fileURLWithPath: a[3]))
