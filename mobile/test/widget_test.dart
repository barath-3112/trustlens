import 'package:flutter_test/flutter_test.dart';
import 'package:trustlens_mobile/main.dart';
void main(){testWidgets('shows TrustLens splash', (tester) async {await tester.pumpWidget(const TrustLensApp());expect(find.text('TrustLens'),findsOneWidget);});}
