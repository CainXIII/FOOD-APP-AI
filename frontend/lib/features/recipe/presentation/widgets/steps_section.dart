import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../../domain/entities/recipe_step.dart';

class StepsSection extends StatefulWidget {
  final List<RecipeStep> steps;

  const StepsSection({
    super.key,
    required this.steps,
  });

  @override
  State<StepsSection> createState() => _StepsSectionState();
}

class _StepsSectionState extends State<StepsSection> {
  int? _expandedStep;

  @override
  Widget build(BuildContext context) {
    if (widget.steps.isEmpty) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(32.0),
          child: Text('Chưa có hướng dẫn nấu'),
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: widget.steps.length,
      itemBuilder: (context, index) {
        final step = widget.steps[index];
        final isExpanded = _expandedStep == index;

        return Card(
          margin: const EdgeInsets.only(bottom: 16),
          child: Column(
            children: [
              ListTile(
                leading: CircleAvatar(
                  backgroundColor: Theme.of(context).primaryColor,
                  child: Text(
                    '${step.stepNumber}',
                    style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                title: Text(
                  step.titleVi ?? 'Bước ${step.stepNumber}',
                  style: const TextStyle(
                    fontWeight: FontWeight.w600,
                  ),
                ),
                subtitle: step.durationMinutes != null
                    ? Row(
                        children: [
                          const Icon(Icons.timer, size: 16),
                          const SizedBox(width: 4),
                          Text('${step.durationMinutes} phút'),
                        ],
                      )
                    : null,
                trailing: Icon(
                  isExpanded ? Icons.expand_less : Icons.expand_more,
                ),
                onTap: () {
                  setState(() {
                    _expandedStep = isExpanded ? null : index;
                  });
                },
              ),
              if (isExpanded) ...[
                // Step Image
                if (step.imageUrl != null) ...[
                  CachedNetworkImage(
                    imageUrl: step.imageUrl!,
                    width: double.infinity,
                    height: 200,
                    fit: BoxFit.cover,
                    placeholder: (context, url) => Container(
                      height: 200,
                      color: Colors.grey[300],
                      child: const Center(child: CircularProgressIndicator()),
                    ),
                    errorWidget: (context, url, error) => Container(
                      height: 200,
                      color: Colors.grey[300],
                      child: const Icon(Icons.image_not_supported, size: 50),
                    ),
                  ),
                  const SizedBox(height: 16),
                ],

                // Instruction
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        step.instructionVi,
                        style: const TextStyle(
                          fontSize: 16,
                          height: 1.5,
                        ),
                      ),

                      // Tips
                      if (step.tipsVi != null && step.tipsVi!.isNotEmpty) ...[
                        const SizedBox(height: 12),
                        Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: Colors.amber[50],
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: Colors.amber[200]!),
                          ),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Icon(
                                Icons.lightbulb_outline,
                                color: Colors.amber[700],
                                size: 20,
                              ),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'Mẹo',
                                      style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        color: Colors.amber[900],
                                      ),
                                    ),
                                    const SizedBox(height: 4),
                                    Text(
                                      step.tipsVi!,
                                      style: TextStyle(
                                        color: Colors.amber[900],
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
              ],
            ],
          ),
        );
      },
    );
  }
}
