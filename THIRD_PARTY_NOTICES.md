# Third-Party Notices and License Map

This is a multi-component research repository. The root MIT license applies only to original code, documentation and modifications for which the repository maintainer holds the necessary rights. It does not replace the licenses of bundled third-party components.

## Component map

| Path | Source / attribution | License or status |
| --- | --- | --- |
| `yolov12-main/` | [sunsmarterjie/yolov12](https://github.com/sunsmarterjie/yolov12), Yunjie Tian and contributors; based in part on Ultralytics | AGPL-3.0. The nested `yolov12-main/LICENSE` controls this component. |
| `yolov12-main/yolov12n.pt` and other model assets | YOLOv12 project and the datasets used to create the weights | Follow the upstream model and dataset terms; these assets are not relicensed by the root MIT license. |
| `stereo_reconstruction_working/` | Some files carry attribution to Panjq / `pan_jinquan@163.com` and cite additional public examples. | Upstream license and canonical source must be verified file by file. The root MIT license covers only the maintainer's original additions and modifications. |
| `hand_eye_download/` | Some files carry the notice “created by Leo Ma at ZJU, 2021.10.05”. | Canonical source and redistribution terms have not been conclusively identified. Preserve attribution and verify permission before separate redistribution or commercial use. |
| `bfg.jar` | BFG Repo-Cleaner binary | Third-party tool; follow the license distributed by the [BFG project](https://github.com/rtyley/bfg-repo-cleaner). |
| Reference PDFs, archived web pages and screenshots | Respective authors, publishers and websites | Not covered by the root MIT license. Their presence is for project reference and does not grant downstream republication rights. |

## Copyleft boundary

Code derived from or combined into the AGPL-covered YOLOv12 program must comply with AGPL-3.0. Keeping an MIT license at the repository root does not convert YOLOv12 or derivative portions to MIT.

## Maintenance rule

For every imported component, record the source URL, version or commit, author, license and modifications. Keep every upstream LICENSE, NOTICE and copyright header.
